from __future__ import annotations

import logging
from typing import Sequence

import torch
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline,
)

from app.domain import DocumentChunk, RagService

logger = logging.getLogger(__name__)


def _device_map() -> str | None:
    """Prefer GPU when available; let HF/Accelerate decide placement."""
    if torch.cuda.is_available():
        return "auto"
    if torch.backends.mps.is_available():
        return "auto"
    return None


class LangChainRagService(RagService):
    """RAG answer generation using a HuggingFace text2text model via LangChain."""

    def __init__(
        self,
        *,
        model_name: str = "google/flan-t5-small",
        max_new_tokens: int = 256,
        temperature: float = 0.0,
    ) -> None:
        device_map = _device_map()
        logger.info("Loading RAG model %s with device_map=%s", model_name, device_map)
        self.llm = HuggingFacePipeline(
            pipeline=_build_generation_pipeline(
                model_name=model_name,
                device_map=device_map,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
            )
        )

    def generate_answer(
        self,
        *,
        question: str,
        context: Sequence[DocumentChunk],
        chat_history: Sequence[tuple[str, str]] | None = None,
    ) -> str:
        _ = chat_history  # Reserved for future use
        context_text = "\n\n".join(
            f"[{idx + 1}] {chunk.content}" for idx, chunk in enumerate(context) if chunk.content
        )
        if not context_text:
            context_text = "No relevant context was retrieved."

        prompt = (
            "You are a helpful assistant. Use the provided context to answer the question. "
            "If the answer is not in the context, say you do not know.\n\n"
            f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer:"
        )
        logger.info(f"[rag] prompt: {prompt}")

        return self.llm.invoke(prompt)


def _build_generation_pipeline(
    *,
    model_name: str,
    device_map: str | None,
    max_new_tokens: int,
    temperature: float,
):
    """Create a HF pipeline that supports both seq2seq (e.g., FLAN) and causal (e.g., LLaMA) models."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    config = AutoConfig.from_pretrained(model_name)

    model_kwargs = {"device_map": device_map} if device_map else {}
    pipeline_kwargs = {
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "do_sample": temperature > 0,
    }

    if config.is_encoder_decoder:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, **model_kwargs)
        task = "text2text-generation"
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
        task = "text-generation"
        # Many chat LLMs have no pad token; align it to EOS for batching/safety.
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.padding_side = "right"
        pipeline_kwargs["return_full_text"] = False
        pipeline_kwargs.setdefault("eos_token_id", tokenizer.eos_token_id)

    return pipeline(
        task=task,
        model=model,
        tokenizer=tokenizer,
        **pipeline_kwargs,
    )
