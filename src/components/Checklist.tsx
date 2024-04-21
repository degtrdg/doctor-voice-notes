import { CheckIcon } from '@heroicons/react/20/solid'

function capitalize(s: string) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

export default function Checklist({ checklist, drugs }: { checklist: any[], drugs: any }) {
    const obj: any = {};
    for (const index in checklist) {
        const item = checklist[index];
        const wordRelation = item?.word_relation;
        const drug = drugs[wordRelation];
        if (!Object.keys(obj).includes(drug)) {
            obj[drug] = []
        }
        obj[drug].push(item);
    }

    return (
        <>
        {
            Object.entries(obj).map(([drug, items], index) => (
                <div key={index} className='flex flex-col gap-3'>
                    <h3 className='text-lg sm:text-xl font-bold text-slate-800'>{capitalize(drug)}</h3>
                    <ul role='list'>
                        {(items as any).sort((a, b) => b.checked - a.checked).map((item, index) => (
                            <li key={index}>
                                <div className="relative pb-8">
                                    {index !== items.length - 1 ? (
                                        <span className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                                    ) : null}
                                    <div className="relative flex space-x-3">
                                        <div>
                                            {
                                                item.checked ? (
                                                    <span className="h-8 w-8 bg-green-500 rounded-full flex items-center justify-center ring-8 ring-white">
                                                        <CheckIcon className="rounded-full flex h-5 w-5 text-white" aria-hidden="true" />
                                                    </span>
                                                ) : (
                                                    <div className="h-8 w-8 bg-gray-100 rounded-full border-[1px]  ring-8 ring-white" />
                                                )
                                            }
                                        </div>
                                        <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                                            <div>
                                                <p className={`font-medium ${item.checked ? "text-gray-400" : "text-gray-800"}`}>
                                                    {item.text}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            ))
        }
        </>
    );
}