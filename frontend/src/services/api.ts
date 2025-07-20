import axios, { AxiosInstance, AxiosResponse } from 'axios';
import type {
  User,
  Feedback,
  FeedbackCreate,
  FeedbackUpdate,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  ManagerDashboard,
  EmployeeDashboard,
} from '@/types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle auth errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', credentials);
    return response.data;
  }

  async register(userData: RegisterData): Promise<User> {
    const response: AxiosResponse<User> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  // User endpoints
  async getUserProfile(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/users/me');
    return response.data;
  }

  async getUser(userId: number): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get(`/users/${userId}`);
    return response.data;
  }

  // Get team members (managers only)
  async getTeamMembers(): Promise<User[]> {
    const response = await this.api.get('/users/team');
    return response.data;
  }

  // Get all managers (for registration)
  async getManagers(): Promise<User[]> {
    const response = await this.api.get('/users/managers');
    return response.data;
  }

  // Feedback endpoints
  async createFeedback(feedback: FeedbackCreate): Promise<Feedback> {
    const response: AxiosResponse<Feedback> = await this.api.post('/feedback/', feedback);
    return response.data;
  }

  async getMyFeedback(): Promise<Feedback[]> {
    const response: AxiosResponse<Feedback[]> = await this.api.get('/feedback/my-feedback');
    return response.data;
  }

  async getEmployeeFeedback(employeeId: number): Promise<Feedback[]> {
    const response: AxiosResponse<Feedback[]> = await this.api.get(`/feedback/employee/${employeeId}`);
    return response.data;
  }

  async getAllFeedback(): Promise<Feedback[]> {
    const response: AxiosResponse<Feedback[]> = await this.api.get('/feedback/');
    return response.data;
  }

  async getFeedback(id: number): Promise<Feedback> {
    const response: AxiosResponse<Feedback> = await this.api.get(`/feedback/${id}`);
    return response.data;
  }

  async updateFeedback(id: number, feedback: FeedbackUpdate): Promise<Feedback> {
    const response: AxiosResponse<Feedback> = await this.api.put(`/feedback/${id}`, feedback);
    return response.data;
  }

  async acknowledgeFeedback(feedbackId: number): Promise<Feedback> {
    const response: AxiosResponse<Feedback> = await this.api.post(`/feedback/${feedbackId}/acknowledge`, {
      acknowledged: true,
    });
    return response.data;
  }

  async addEmployeeComment(feedbackId: number, comment: string): Promise<Feedback> {
    const response: AxiosResponse<Feedback> = await this.api.post(`/feedback/${feedbackId}/comment`, {
      employee_comment: comment,
    });
    return response.data;
  }

  // Dashboard endpoints
  async getManagerDashboard(): Promise<ManagerDashboard> {
    const response: AxiosResponse<ManagerDashboard> = await this.api.get('/dashboard/manager');
    return response.data;
  }

  async getEmployeeDashboard(): Promise<EmployeeDashboard> {
    const response: AxiosResponse<EmployeeDashboard> = await this.api.get('/dashboard/employee');
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService;
