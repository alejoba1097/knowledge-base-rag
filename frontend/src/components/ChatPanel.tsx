import { FormEvent, useEffect, useRef, useState } from 'react';

export type ChatMessage = {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
};

export type ChatPanelProps = {
  messages: ChatMessage[];
  disabled?: boolean;
  isSending: boolean;
  onSend: (content: string) => Promise<void> | void;
};

export function ChatPanel({ messages, disabled = false, isSending, onSend }: ChatPanelProps) {
  const [draft, setDraft] = useState('');
  const chatWindowRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const container = chatWindowRef.current;
    if (!container) return;
    container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = draft.trim();
    if (!trimmed || disabled || isSending) return;

    setDraft('');
    void onSend(trimmed);
  };

  return (
    <section className="panel chat-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Ask grounded questions</p>
          <h2>Chat with your document</h2>
          <p className="muted">Once your PDF is indexed, the assistant will answer only from that source.</p>
        </div>
        {disabled && <span className="status-badge status-idle">Waiting for upload</span>}
      </div>

      <div className="chat-window" role="log" aria-live="polite" ref={chatWindowRef}>
        {messages.map((message) => (
          <article key={message.id} className={`chat-bubble role-${message.role}`}>
            <p className="chat-role">{message.role === 'assistant' ? 'Assistant' : message.role === 'user' ? 'You' : 'System'}</p>
            <p>{message.content}</p>
          </article>
        ))}
        {isSending && <div className="chat-bubble role-assistant pending">Thinking…</div>}
      </div>

      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder={disabled ? 'Upload a PDF to start asking questions' : 'Ask something specific from your PDF…'}
          disabled={disabled}
          aria-label="Chat prompt"
        />
        <button type="submit" className="primary" disabled={disabled || isSending || !draft.trim()}>
          {isSending ? 'Sending…' : 'Send'}
        </button>
      </form>
    </section>
  );
}

export default ChatPanel;
