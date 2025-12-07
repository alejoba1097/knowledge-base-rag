import { useMemo, useState } from 'react';
import ChatPanel, { type ChatMessage } from './components/ChatPanel';
import UploadPanel, { type UploadStatus } from './components/UploadPanel';
import { API_BASE_URL } from './config';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const seedMessages: ChatMessage[] = [
  {
    id: 'intro',
    role: 'system',
    content: 'Upload a PDF to ground the assistant. Answers will stick to the indexed document.',
  },
];

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>('idle');
  const [uploadStatusMessage, setUploadStatusMessage] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>(seedMessages);
  const [isSending, setIsSending] = useState(false);

  const isChatDisabled = useMemo(() => uploadStatus !== 'ready', [uploadStatus]);

  const handleFileSelect = (nextFile: File | null) => {
    setFile(nextFile);
    setUploadStatus('idle');
    setUploadStatusMessage(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploadStatus('uploading');
    setUploadStatusMessage('Uploading and indexing your PDF…');
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }
      const result = (await response.json()) as { document_id: string; filename: string };
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

    await delay(650);

    const assistantMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content:
        uploadStatus === 'ready'
          ? `Placeholder response referencing ${file?.name ?? 'your document'}. Connect to your backend to stream real answers grounded in the uploaded PDF.`
          : 'Upload and index a PDF to unlock grounded answers.',
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setIsSending(false);
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
