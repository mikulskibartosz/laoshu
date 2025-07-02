import apiClient from "./api";

export interface Claim {
  claim: string;
  sources: string[];
  is_correct: boolean;
}

export const verifyAI = async (text: string): Promise<Claim[]> => {
  try {
    const response = await apiClient.post("/check", {
      text: text,
      only_incorrect: false,
    });

    return response.data;
  } catch (error) {
    console.error("Error verifying AI content:", error);
    throw error;
  }
};
