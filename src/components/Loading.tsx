import { ArrowPathIcon } from '@heroicons/react/24/outline';


export default function Loading() {
    return (
        <div className="flex justify-center items-center h-screen text-xl">
            <ArrowPathIcon className='h-8 w-8 animate-spin' />&nbsp;Loading...
        </div>
    );
}