"use client"
import Checklist from "@/components/Checklist";
import Transcript from "@/components/Transcript";
import { useEffect, useState } from "react";
import { ref } from "firebase/database";
import { database } from "@/firebase";
import { useObjectVal } from "react-firebase-hooks/database";
import Loading from "@/components/Loading";

export default function Page({ params }: { params: { slug: string } }) {
  const [sessionID, setSessionID] = useState<number>(1);
  const [value, loading, error] = useObjectVal(ref(database, '/'));
  const [transcription, setTranscription] = useState([]);
  const [checklist, setChecklist] = useState([]);

  useEffect(() => {
    setSessionID(parseInt(params.slug))
  }, [])

  useEffect(() => {
    if (value) {
      const sessions = (value as any)["Session"]
      
      if (0 < sessionID < sessions.length) {
        const session = sessions[sessionID]
        setTranscription(Object.values(session["Transcript"]))
        setChecklist(Object.values(session["Checklist"]))
      }
    }
  }, [value])

  return loading ? (
    <Loading />
  ) : (
    <div className="flex h-screen">
      <div className="flex flex-col gap-4 pt-4 pl-8 pr-10">
        <h2 className="inline-block text-xl sm:text-2xl font-bold text-slate-800">
          Session Transcript
        </h2>
        <Transcript transcript={transcription} />
        
      </div>

      <div className="flex gap-10">
        <div className="bg-gray-200 w-[1.5px] rounded-full" />

        <div className="flex flex-col gap-6 pt-4 pr-6">
          <h2 className="inline-block text-xl sm:text-2xl font-bold text-slate-800">
          Patient Prescription Checklist
          </h2>
          <Checklist checklist={checklist} />
        </div>
      </div>
    </div>
  );

}