"use client"
import { useEffect, useState } from "react";

export default function Page() {
  const [sessionID, setSessionID] = useState(1);
  const [transcription, setTranscription] = useState([]);
  const hostname = "http://localhost:8000";

  useEffect(() => {
    console.log("Page component mounted");
    async function fetchData() {
      const response = await fetch(`${hostname}/api/all_transcripts/${sessionID}`);
      const jsonData = await response.json();
      const text = jsonData.message.diarization
      const transcription = text.split("\n").map((line: string) => line.split(": "));
      setTranscription(transcription);
    }

    fetchData();
  }, []);

  return (
    <div className="flex justify-around">

      <div>
        <h2>Conversation Transcription</h2>
        <div className="lg:overflow-y-auto">
          {transcription.map((line, index) => (
            <div key={index}>
              <p className="text-md">
                <span className={`font-semibold capitalize ${(line[0] as string).toLowerCase() == "doctor" ? "text-blue-600" : "text-slate-900"}`}>{line[0]}: </span>
                {line[1]}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2>Checklist</h2>
        <ul>
          <li>Get the session ID</li>
          <li>Fetch the data from the server</li>
          <li>Display the data</li>
        </ul>
      </div>
    </div>
  );

}