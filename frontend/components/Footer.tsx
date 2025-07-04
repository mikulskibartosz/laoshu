import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-base-200 border-t border-base-content/10 fixed bottom-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-8 py-12">
        <div className="text-center">
          <p className="text-sm text-base-content/80">
            Built by{" "}
            <a
              href="https://mikulskibartosz.name"
              target="_blank"
              rel="noopener noreferrer"
              className="link link-hover font-semibold"
            >
              Bartosz Mikulski
            </a>{" "}
            — AI hallucination-prevention specialist delivering rapid MVPs, seamless LLM integration, and production-grade reliability fixes.<br/>
            Lǎoshǔ found an issue you can&apos;t squash? <a href="https://mikulskibartosz.name/about" className="link link-hover font-semibold">Reach out for a custom solution.</a>
          </p>
          <p className="mt-3 text-sm text-base-content/60">
          Lǎoshǔ.ai is released under the GNU Affero General Public License v3.0. Commercial entities wishing to use it under a different license should contact me.
          <br/>
          <Link href="/privacy-policy" className="link link-hover font-semibold">Privacy Policy</Link> | <Link href="/tos" className="link link-hover font-semibold">Terms of Service</Link> | <Link href="https://github.com/mikulskibartosz/laoshu" className="link link-hover font-semibold">Source Code</Link> | <Link href="https://laoshu.ai" className="link link-hover font-semibold">Project Website</Link>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
