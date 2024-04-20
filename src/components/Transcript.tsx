export default function Transcript({ transcript }: { transcript: any[] }) {
    return (
        <div className="flex flex-col gap-3 lg:overflow-y-auto">
            {transcript.map((line, index) => (
                <div key={index}>
                    <p className="text-md text-justify text-slate-800">
                        <span className={`font-semibold capitalize 
                ${(line.user as string).toLowerCase() == "doctor" ? "text-blue-600" : "text-emerald-700"}`}>
                            {line.user}:&nbsp;
                        </span>
                        <span>{line.text}</span>
                    </p>
                </div>
            ))}
        </div>
    );
}