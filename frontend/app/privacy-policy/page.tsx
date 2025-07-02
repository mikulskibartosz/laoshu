import Link from "next/link";
import config from "@/config";

const PrivacyPolicy = () => {
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
          Privacy Policy for {config.appName}
        </h1>

        <pre
          className="leading-relaxed whitespace-pre-wrap"
          style={{ fontFamily: "sans-serif" }}
        >
          {`Last Updated: 2025-07-03

Thank you for using Lǎoshǔ.ai ("we," "us," or "our"). This Privacy Policy outlines our commitment to privacy and data protection when you use our application.

By using Lǎoshǔ.ai, you agree to the terms of this Privacy Policy. If you do not agree with the practices described in this policy, please do not use the application.

1. Information We Collect

1.1 No Personal Data Collection

Lǎoshǔ.ai itself does not collect, store, or process any personal information on our servers. However, to provide our fact-checking service, we send the text you provide to third-party services for processing.

1.2 No Non-Personal Data Collection

We do not use web cookies, tracking technologies, or any other means to collect non-personal information such as IP addresses, browser types, device information, or browsing patterns. Your usage of Lǎoshǔ.ai remains completely private and untracked on our end.

2. Third-Party Services

2.1 Data Processing Services

To verify the accuracy of claims in your text, Lǎoshǔ.ai sends your content to the following third-party services:

- ScrapingAnt: Used to scrape and retrieve content from web sources for fact-checking purposes
- OpenAI: Used to analyze and verify claims against the retrieved information

2.2 Third-Party Privacy Policies

When you use Lǎoshǔ.ai, your text content is processed by these third-party services according to their respective privacy policies. We recommend reviewing their privacy policies:

- ScrapingAnt Privacy Policy: https://scrapingant.com/legal/privacy-policy/
- OpenAI Privacy Policy: https://openai.com/privacy

3. Purpose of Data Processing

The text you provide is processed solely for the purpose of fact-checking and verifying claims against publicly available information. We do not use your content for any other purposes.

4. Data Retention

Lǎoshǔ.ai does not store your submitted text on our servers. However, third-party services may retain data according to their own policies. Please refer to their privacy policies for details on data retention.

5. Children's Privacy

Lǎoshǔ.ai is not intended for children under the age of 13. Please ensure that any content submitted does not contain personal information of children under 13.

6. Updates to the Privacy Policy

We may update this Privacy Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons. Any updates will be posted on this page.

7. Contact Information

If you have any questions, concerns, or requests related to this Privacy Policy, you can contact us at:

Email: Please create a GitHub issue at {config.repositoryUrlNewIssue}

For all other inquiries, please visit our website at https://laoshu.ai.

By using Lǎoshǔ.ai, you acknowledge that your text content will be sent to third-party services for processing and agree to their respective privacy policies.`}
        </pre>
      </div>
    </main>
  );
};

export default PrivacyPolicy;
