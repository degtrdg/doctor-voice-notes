"use client"
import { useEffect, useState } from "react";
import { useObjectVal } from "react-firebase-hooks/database";
import { ref } from "firebase/database";
import { database } from "@/firebase";
import Loading from "@/components/Loading";
import Link from 'next/link';


export default function Page() {
    const [value, loading, error] = useObjectVal(ref(database, '/'));
    const [sessions, setSessions] = useState([]);

    useEffect(() => {
        if (value) {
            setSessions(Object.values(value["Session"]));
        }
    }, [value]);
    console.log(sessions);
    return loading ? (
        <Loading />
    ) : (
        <div className="p-8 max-w-3xl mx-auto">
            <div className="flex flex-col gap-8">
                <h1 className="text-center inline-block text-xl sm:text-2xl font-bold text-slate-800">
                    Patient Sessions
                </h1>
                <div className="h-[1.5px] w-full bg-gray-300" />
                <div>
                    {
                        sessions.map((session, index) => (
                            <Link key={index} className="text-center inline-block w-full py-3 px-6 bg-blue-500 text-white font-bold rounded shadow-sm hover:bg-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 transition" href={`\\session\\${index + 1}`}>
                                Session {session["name"]}
                            </Link>
                        ))
                    }
                </div>
            </div>
        </div>
    );
}