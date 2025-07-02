import Link from "next/link";
import config from "@/config";

const TOS = () => {
  return (
    <main className="max-w-xl mx-auto">
      <div className="p-5">
        <Link href="/" className="btn btn-ghost">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            className="w-5 h-5"
          >
            <path
              fillRule="evenodd"
              d="M15 10a.75.75 0 01-.75.75H7.612l2.158 1.96a.75.75 0 11-1.04 1.08l-3.5-3.25a.75.75 0 010-1.08l3.5-3.25a.75.75 0 111.04 1.08L7.612 9.25h6.638A.75.75 0 0115 10z"
              clipRule="evenodd"
            />
          </svg>{" "}
          Back
        </Link>
        <h1 className="text-3xl font-extrabold pb-6">
          Terms and Conditions for {config.appName}
        </h1>

        <pre
          className="leading-relaxed whitespace-pre-wrap"
          style={{ fontFamily: "sans-serif" }}
        >
          {`Last Updated: 2025-07-03

Welcome to Lǎoshǔ.ai!

These Terms of Service ("Terms") govern your use of the Lǎoshǔ.ai website and the fact-checking services provided by Lǎoshǔ.ai. By using our website and services, you agree to these Terms.

1. Description of Lǎoshǔ.ai

Lǎoshǔ.ai is an AI-powered fact-checking platform that helps users verify the accuracy of claims in their text content by analyzing it against publicly available information.

2. Service Usage

Lǎoshǔ.ai provides fact-checking services by processing text content you submit. The service is provided "as is" and we make no guarantees regarding the accuracy or completeness of fact-checking results.

3. User Responsibilities

You are responsible for:
- Ensuring you have the right to submit any content for fact-checking
- Not submitting content that violates any laws or third-party rights
- Understanding that fact-checking results are for informational purposes only
- Not relying solely on our service for critical decisions

4. Intellectual Property

You retain ownership of any content you submit. By using our service, you grant us a limited license to process your content solely for the purpose of providing fact-checking services.

5. Third-Party Services

Our fact-checking service relies on third-party services (ScrapingAnt and OpenAI). Your use of our service is also subject to their respective terms of service and privacy policies.

6. Limitation of Liability

Lǎoshǔ.ai is provided free of charge and without warranties. We are not liable for any damages arising from your use of our service or reliance on fact-checking results.

7. Privacy

Your privacy is important to us. Please review our Privacy Policy at /privacy-policy to understand how we handle your data.

8. Open Source License

Lǎoshǔ.ai is released under the GNU Affero General Public License v3.0. Commercial entities wishing to use it under a different license should contact the developer.

9. Governing Law

These Terms are governed by the laws of Poland. Any disputes arising from these Terms or your use of our service will be subject to the exclusive jurisdiction of the courts of Poland.

10. Updates to the Terms

We may update these Terms from time to time. Continued use of our service constitutes acceptance of updated terms.

11. Contact Information

For questions about these Terms, please create a GitHub issue at ${config.repositoryUrlNewIssue}.

For all other inquiries, please visit our website at https://laoshu.ai.

Thank you for using Lǎoshǔ.ai!`}
        </pre>
      </div>
    </main>
  );
};

export default TOS;
