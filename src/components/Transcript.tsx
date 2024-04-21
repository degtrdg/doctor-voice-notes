import { useState, useEffect } from "react";
import Typewriter from "@/components/Typewriter";

interface TranscriptProps {
    transcript: any[];
    currentLine: number;
    setCurrentLine: any;
}

export default function Transcript({ transcript, currentLine, setCurrentLine }: TranscriptProps) {
    const [currentLines, setCurrentLines] = useState<any[]>([]);

    useEffect(() => {
        if (transcript.length > 0) {
            setCurrentLines(transcript.slice(0, currentLine))
        }
    }, [transcript, currentLine])

    const handleComplete = () => {
        if (currentLine < transcript.length - 1) {
            setCurrentLine((currentLine: number) => currentLine + 1);
        }
    };

    return (
        <div className="flex flex-col gap-3">
            {transcript.map((line, index) => (
                <div key={index}>
                    <p className="text-md text-justify text-slate-800">
                        <span className={`font-semibold capitalize ${(line?.user as string).toLowerCase() == "doctor" ? "text-blue-600" : "text-emerald-700"}`}>
                            {line.user}:{" "}
                        </span>
                        <Typewriter text={line.text} speed={30} onComplete={handleComplete} />
                        {/* {line.text} */}
                    </p>
                </div>
            ))}
        </div>
    );
}