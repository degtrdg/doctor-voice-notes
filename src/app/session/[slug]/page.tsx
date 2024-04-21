"use client"
import Checklist from "@/components/Checklist";
import Transcript from "@/components/Transcript";
import { HomeIcon } from '@heroicons/react/20/solid'
import { useEffect, useState } from "react";
import { ref, set } from "firebase/database";
import { database } from "@/firebase";
import { useObjectVal } from "react-firebase-hooks/database";
import Loading from "@/components/Loading";
import Logo from "@/components/Logo";
import Link from 'next/link';
import Navbar from "@/components/Navbar";

export default function Page({ params }: { params: { slug: string } }) {
  const sessionID = params.slug;
  const [value, loading, error] = useObjectVal(ref(database, '/'));
  const [transcription, setTranscription] = useState([]);
  const [checklist, setChecklist] = useState([]);
  const [drugs, setDrugs] = useState<any[]>([]);
  const [currentLine, setCurrentLine] = useState<number>(0);

  useEffect(() => {
    if (value) {
      const sessions = (value as any)["Session"]
      const sessionsKeys = Object.keys(sessions)

      if (sessionsKeys.includes(sessionID)) {
        const session = sessions[sessionID]
        const sessionKeys = Object.keys(session)

        if (sessionKeys.includes("Transcript")) {
          setTranscription(Object.values(session["Transcript"]))
        }

        if (sessionKeys.includes("Checklist")) {
          setChecklist(Object.values(session["Checklist"]))
        }

        if (sessionKeys.includes("Drugs")) {
          setDrugs(Object.values(session["Drugs"]))
        }

        if (currentLine == 0) {
          setCurrentLine(0)
        }
      }
    }
  }, [value])

  if (loading) return <Loading />

  return (
    <div className="max-h-full">
      <Navbar />

      <div className="flex h-screen">
        <div className="flex-1 flex grid-cols-2 flex-col gap-4 pt-8 pl-9 pr-10">
          <h2 className="inline-block text-xl sm:text-2xl font-bold text-slate-800">
            Session Transcript
          </h2>
          <Transcript transcript={transcription} currentLine={currentLine} setCurrentLine={setCurrentLine} />
        </div>

        <div className="flex gap-10">
          <div className="bg-gray-200 w-[1.5px] rounded-full" />

          <div className="flex flex-col gap-6 pt-8 pr-9">
            <h2 className="inline-block text-xl sm:text-2xl font-bold text-slate-800">
              Patient Prescription Checklist
            </h2>
            <Checklist checklist={checklist} drugs={drugs} />
          </div>
        </div>
      </div>
    </div>
  );

}