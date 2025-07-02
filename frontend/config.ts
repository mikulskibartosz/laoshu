import themes from "daisyui/src/theming/themes";
import { ConfigProps } from "./types/config";

const config = {
  appName: "Lǎoshǔ.ai",
  appDescription:
    "Lǎoshǔ.ai is a platform for verifying the accuracy of AI.",
  domainName: "laoshu.ai",
  colors: {
    theme: "light",
    main: themes["light"]["primary"],
  },
  backendUrl: process.env.BACKEND_URL || "http://localhost:8000",
  repositoryUrlNewIssue: "https://github.com/mikulskibartosz/laoshu/issues/new",
} as ConfigProps;

export default config;
