import { CheckIcon } from '@heroicons/react/20/solid'

export default function Checklist({ checklist }: { checklist: any[] }) {
    return (
        <ul role="list">
            {checklist.sort((a, b) => b.checked - a.checked).map((item, index) => (
                <li key={index}>
                    <div className="relative pb-8">
                        {index !== checklist.length - 1 ? (
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
    );
}