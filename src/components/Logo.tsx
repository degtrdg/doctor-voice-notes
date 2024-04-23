import Link from 'next/link';
import "./logo.css";

interface LogoProps {
    isLink?: boolean;
    whiteText?: boolean;
}

export default function Logo({ isLink = true, whiteText = false }: LogoProps) {
    const style = "flex items-center text-lg md:text-xl text-slate-700 font-display font-medium tracking-tight";

    if (isLink) return (
        <Link href={"/"} className={style}>
            <img src="/medical_clipboard-512.png" className="logo inline-block h-9 w-9 mr-1" />
            <span className={`${whiteText ? "text-white" : "text-slate-800"} font-bold text-xl`}>PreScribe</span>
        </Link>
    );

    return (
        <div className={style}>
            <img src="/logo.svg" className="logo inline-block h-8 w-8 mr-1" />
            <span>PreScribe</span>
        </div>
    );
}