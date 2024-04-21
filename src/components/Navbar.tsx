import Logo from "@/components/Logo";

const user = {
    name: 'Tom Cook',
    email: 'tom@example.com',
    imageUrl:
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
};

export default function Navbar() {
    return (
        <div className="py-6 px-6 bg-blue-800 shadow-md">
            <div className="flex items-center justify-between">
                <Logo whiteText={true} />
                <div className="flex items-center gap-3">
                    <span className="text-md font-medium text-white">Dr. {user.name}</span>
                    <img className="h-10 w-10 rounded-full" src={user.imageUrl} alt="" />
                </div>
            </div>
        </div>
    );
}