export interface User {
  id: number
  name: string
  email: string
  role: 'manager' | 'employee'
  manager_id?: number
  created_at: string
  manager?: User
}

export interface Feedback {
  id: number
  employee_id: number
  manager_id: number
  strengths: string
  areas_to_improve: string
  sentiment: 'positive' | 'neutral' | 'negative'
  created_at: string
  updated_at?: string
  acknowledged: boolean
  acknowledged_at?: string
  tags?: string
  is_anonymous: boolean
  employee_comment?: string
  employee?: User
  manager?: User
}

export interface FeedbackCreate {
  employee_id: number
  strengths: string
  areas_to_improve: string
  sentiment: 'positive' | 'neutral' | 'negative'
  tags?: string
  is_anonymous?: boolean
}

export interface FeedbackUpdate {
  strengths?: string
  areas_to_improve?: string
  sentiment?: 'positive' | 'neutral' | 'negative'
  tags?: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  name: string
  email: string
  password: string
  role: 'manager' | 'employee'
  manager_id?: number
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface DashboardStats {
  total_feedback: number
  positive_feedback: number
  neutral_feedback: number
  negative_feedback: number
  recent_feedback: Feedback[]
}

export interface ManagerDashboard extends DashboardStats {
  team_size: number
  team_members: User[]
}

export interface EmployeeDashboard extends DashboardStats {
  unacknowledged_feedback: number
}

export interface ApiError {
  detail: string
}
