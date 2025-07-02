"use client";

import Link from "next/link";
import Image from "next/image";
import logo from "@/app/icon.png";

const Header = () => {
  return (
    <header className="bg-white border-b border-base-content/10">
      <nav
        className="container flex items-center justify-between px-8 py-4 mx-auto"
        aria-label="Global"
      >
        <div className="flex items-center gap-2">
          <Link
            className="flex items-center gap-2 shrink-0"
            href="/"
            title="Lǎoshǔ.ai homepage"
          >
            <Image
              src={logo}
              alt="Lǎoshǔ.ai logo"
              className="w-8"
              priority={true}
              width={32}
              height={32}
            />
            <h1 className="font-extrabold text-lg">Lǎoshǔ.ai</h1>
          </Link>
        </div>
      </nav>

      <div className="container mx-auto px-8 pb-4">
        <h2 className="text-left text-base-content/80 text-sm">
          Instantly checks every citation in your GPT-4 or Perplexity output and flags the fakes before they fool you.
        </h2>
      </div>
    </header>
  );
};

export default Header;
