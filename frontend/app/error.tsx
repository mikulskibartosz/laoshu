"use client";

import Image from "next/image";

export default function Error({
  error,
}: {
  error: Error;
}) {
  return (
    <>
      <div className="h-screen w-full flex flex-col justify-center items-center text-center gap-6 p-6">
        <div className="p-6 bg-white rounded-xl">
          <Image
            src="/icon.png"
            alt="App Icon"
            width={144}
            height={144}
            className="w-36 h-36 md:w-64 md:h-64"
          />
        </div>

        <p className="font-medium md:text-xl md:font-semibold">
          Something went wrong 🥲
        </p>

        <p className="text-red-500">{error?.message}</p>

      </div>
    </>
  );
}
