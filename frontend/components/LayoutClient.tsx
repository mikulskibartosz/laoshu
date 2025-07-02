"use client";

import { ReactNode } from "react";
import NextTopLoader from "nextjs-toploader";
import { Toaster } from "react-hot-toast";
import { Tooltip } from "react-tooltip";
import config from "@/config";

const ClientLayout = ({ children }: { children: ReactNode }) => {
  return (
    <>
        <NextTopLoader color={config.colors.main} showSpinner={false} />

        {children}

        <Toaster
          toastOptions={{
            duration: 3000,
          }}
        />

        <Tooltip
          id="tooltip"
          className="z-[60] !opacity-100 max-w-sm shadow-lg"
        />
    </>
  );
};

export default ClientLayout;
