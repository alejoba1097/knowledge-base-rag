import { useEffect, useMemo, useState } from 'react';
import ChatPanel, { type ChatMessage } from './components/ChatPanel';
import UploadPanel, { type UploadStatus } from './components/UploadPanel';
import { API_BASE_URL } from './config';

type ChatResponse = { answer: string; source?: string | null };

const seedMessages: ChatMessage[] = [
  {
    id: 'intro',
    role: 'system',
    content: 'Upload a PDF to ground the assistant. Answers will stick to the indexed document.',
  },
];

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>('idle');
  const [uploadStatusMessage, setUploadStatusMessage] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>(seedMessages);
  const [isSending, setIsSending] = useState(false);

  const isChatDisabled = useMemo(() => uploadStatus !== 'ready', [uploadStatus]);

  useEffect(() => {
    const controller = new AbortController();

    const checkHealth = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/health`, { signal: controller.signal });
        if (response.ok) {
          const body = await response.json();
          console.log('[health] backend reachable:', body);
        }
      } catch (error) {
        if ((error as Error).name !== 'AbortError') {
          console.warn('[health] backend unreachable:', error);
        }
      }
    };

    void checkHealth();

    return () => controller.abort();
  }, []);

  const handleFileSelect = (nextFile: File | null) => {
    setFile(nextFile);
    setDocumentId(null);
    setUploadStatus('idle');
    setUploadStatusMessage(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploadStatus('uploading');
    setUploadStatusMessage('Uploading and indexing your PDF…');
    try {
      const uploadContext = { name: file.name, size: file.size, type: file.type, apiUrl: `${API_BASE_URL}/upload` };
      console.log('[upload] starting upload', uploadContext);
      const formData = new FormData();
      console.log('[upload] preparing to append file to form data');
      formData.append('file', file);
      console.log('[upload] preparing to fetch upload endpoint');
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      console.log('[upload] response status', response.status);
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }
      const result = (await response.json()) as { document_id: string; filename: string };
      console.log('[upload] success', result);
      setDocumentId(result.document_id);
      setUploadStatus('ready');
      const message = `${result.filename} is ready. Ask questions to get grounded answers.`;
      setUploadStatusMessage(message);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'system',
          content: `Indexed ${result.filename}. Stream answers from your backend here.`,
        },
      ]);
    } catch (error) {
      console.error('[upload] error', error);
      setUploadStatus('error');
      const message = error instanceof Error ? error.message : 'Upload failed. Please try again.';
      setUploadStatusMessage(message);
    }
  };

  const handleSend = async (content: string) => {
    const trimmed = content.trim();
    if (!trimmed) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsSending(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed, document_id: documentId }),
      });
      if (!response.ok) {
        throw new Error(`Chat failed: ${response.status}`);
      }
      const result = (await response.json()) as ChatResponse;
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: result.answer,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Chat failed. Please try again.';
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `Could not get an answer: ${message}`,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="backdrop" aria-hidden />
      <header className="hero">
        <div className="hero-text">
          <p className="eyebrow">Knowledge Base RAG</p>
          <h1>Upload a PDF and chat with it</h1>
          <p className="muted">
            A focused playground for your Retrieval-Augmented Generation flow. Index a document, then ask questions that stay grounded in the source.
          </p>
          <div className="hero-tags">
            <span className="pill">PDF ingestion</span>
            <span className="pill">Chunk & embed ready</span>
            <span className="pill">Chat UX</span>
          </div>
        </div>
        <div className="hero-cta">
          <p className="muted">Frontend in React + TypeScript. Wire up your API when the backend is ready.</p>
        </div>
      </header>

      <main className="layout">
        <UploadPanel
          file={file}
          status={uploadStatus}
          statusMessage={uploadStatusMessage}
          onFileSelect={handleFileSelect}
          onUpload={handleUpload}
        />
        <ChatPanel messages={messages} disabled={isChatDisabled} isSending={isSending} onSend={handleSend} />
      </main>
    </div>
  );
}

export default App;
