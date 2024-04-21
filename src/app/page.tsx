"use client"
import { useEffect, useState } from "react";
import { useObjectVal } from "react-firebase-hooks/database";
import { ref } from "firebase/database";
import { database } from "@/firebase";
import Loading from "@/components/Loading";
import Link from 'next/link';
import Navbar from "@/components/Navbar";

export default function Page() {
    const [value, loading, error] = useObjectVal(ref(database, '/'));
    const [sessions, setSessions] = useState([]);

    useEffect(() => {
        if (value) {
            setSessions((value as any)["Session"]);
        }
    }, [value]);
    if (loading) return <Loading />;

    return (
        <div className="mx-auto">
            <Navbar />

            <div className="mt-6">
                <h1 className="text-center text-xl sm:text-2xl font-medium text-slate-800 mb-6">
                    Transcription Sessions
                </h1>
                <div className="flex flex-col gap-4 max-w-3xl mx-auto">
                    {
                        Object.entries(sessions)
                            .sort((a, b) => b[1].name > a[1].name)
                            .map(([sessionKey, session], index) => (
                                <Link key={index} className="text-center inline-block w-full py-3 px-6 bg-blue-700 text-white font-bold rounded shadow-md hover:bg-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 transition"
                                    href={`\\session\\${sessionKey}`}>
                                    Session {session["name"]}
                                </Link>
                            ))
                    }
                </div>
            </div>
        </div>
    );
}