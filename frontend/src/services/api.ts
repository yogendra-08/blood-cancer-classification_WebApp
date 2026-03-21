// API base URL - update this to match your server
export const API_BASE_URL = 'http://10.73.212.36:5000';

export interface PredictionResult {
  success: boolean;
  prediction: {
    class: string;
    confidence: number;
    all_probabilities: Record<string, number>;
  };
  gradcam_url: string;
  timestamp: string;
}

export const uploadImage = async (file: File): Promise<PredictionResult> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const checkHealth = async (): Promise<{ status: string; model_loaded: boolean }> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};
