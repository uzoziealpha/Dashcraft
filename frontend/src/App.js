import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [userMessage, setUserMessage] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!file) {
      setError('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5001/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        setFileId(data.file_id);
        setError('');
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('File upload failed');
    }
  };

  const sendMessageToAI = async () => {
    if (!userMessage) {
      setError('Message is required');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          file_id: fileId,
        }),
      });

      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setAiResponse(data.choices[0].message.content);
        setError('');
      }
    } catch (err) {
      setError('Chat request failed');
    }
  };

  return (
    <div>
      <h1>AI Data Ingestion Test</h1>

      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload File</button>

      {fileId && <p>File uploaded successfully. File ID: {fileId}</p>}

      <textarea
        placeholder="Type a message for the AI agent"
        value={userMessage}
        onChange={(e) => setUserMessage(e.target.value)}
      />
      <button onClick={sendMessageToAI}>Send to AI</button>

      {aiResponse && <div><h3>AI Response:</h3><p>{aiResponse}</p></div>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default App;