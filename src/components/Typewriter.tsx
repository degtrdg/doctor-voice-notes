import { use, useEffect, useState } from 'react';

interface TypewriterProps {
  text: string; 
  speed?: number; 
  onComplete?: any;
}

export default function Typewriter({ text, speed = 100, onComplete = () => {} }: TypewriterProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < text.length) {
      const timer = setTimeout(() => {
        setDisplayedText((prev) => prev + text.charAt(index));
        setIndex((prev) => prev + 1);
      }, speed);
      return () => clearTimeout(timer);
    } 
  }, [index, text, speed]);

  useEffect(() => {
    if (index === text.length) {
      onComplete();
    }
  }, [index]);

  return <span>{displayedText}</span>;
}