# Internal Feedback Tool - Frontend

A modern Vue.js frontend for the Internal Feedback Tool, providing a clean and intuitive interface for managers and employees to share structured feedback.

## 🚀 Features

### Authentication & Authorization
- **Secure Login/Registration** with JWT token management
- **Role-based Access Control** (Manager/Employee)
- **Automatic Token Refresh** and session management
- **Protected Routes** with authentication guards

### Manager Features
- **Dashboard Overview** with team statistics and recent feedback
- **Create Feedback** with structured forms (strengths, areas to improve, sentiment)
- **Edit Feedback** with full CRUD capabilities
- **Team Management** view with team member feedback status
- **Feedback History** with filtering and search capabilities

### Employee Features
- **Personal Dashboard** with feedback summary and acknowledgment status
- **Feedback Review** with ability to acknowledge and comment
- **Feedback History** with personal feedback timeline
- **Profile Management** with account details

### UI/UX Features
- **Responsive Design** optimized for desktop and mobile
- **Modern Interface** using Tailwind CSS design system
- **Loading States** and error handling throughout
- **Real-time Updates** with optimistic UI patterns
- **Accessibility** compliant with WCAG guidelines

## 🛠 Tech Stack

- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Vite** for fast development and building
- **Tailwind CSS** for utility-first styling
- **Pinia** for state management
- **Vue Router** for client-side routing
- **Axios** for API communication
- **Heroicons** for consistent iconography

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000`

### Setup Steps

1. **Clone and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open in browser**
   ```
   http://localhost:5173
   ```

## 🏗 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable Vue components
│   ├── views/            # Page components
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DashboardView.vue
│   │   ├── FeedbackView.vue
│   │   ├── CreateFeedbackView.vue
│   │   ├── EditFeedbackView.vue
│   │   ├── TeamView.vue
│   │   └── ProfileView.vue
│   ├── stores/           # Pinia stores
│   │   └── auth.ts       # Authentication state
│   ├── services/         # API services
│   │   └── api.ts        # Axios API client
│   ├── router/           # Vue Router config
│   │   └── index.ts      # Route definitions
│   ├── types/            # TypeScript definitions
│   │   └── index.ts      # Type definitions
│   ├── style.css         # Global styles
│   └── main.ts           # App entry point
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind CSS config
└── tsconfig.json         # TypeScript config
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend root:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### API Proxy
The Vite config includes a proxy for API requests:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## 🎨 Design System

### Colors
- **Primary**: Blue tones for main actions and branding
- **Success**: Green for positive feedback and confirmations
- **Warning**: Yellow for neutral feedback and alerts
- **Danger**: Red for negative feedback and errors
- **Gray**: Neutral tones for text and backgrounds

### Components
- **Cards**: Consistent container styling
- **Buttons**: Primary, secondary, and danger variants
- **Forms**: Standardized input styling with validation
- **Badges**: Status indicators with color coding
- **Modals**: Overlay components for interactions

## 🔐 Authentication Flow

1. **Registration**: Users register with role selection (Manager/Employee)
2. **Login**: JWT token received and stored in localStorage
3. **Token Management**: Automatic injection in API requests
4. **Route Guards**: Protected routes check authentication status
5. **Role-based Access**: Different UI based on user role

## 📱 Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Tablet Support**: Adapted layouts for tablet screens
- **Desktop Enhanced**: Full feature set on desktop
- **Touch Friendly**: Large touch targets and gestures

## 🧪 Development

### Available Scripts

```bash
# Development server
npm run dev

# Type checking
npm run type-check

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Code Style
- **TypeScript** for type safety
- **ESLint** for code quality
- **Prettier** for code formatting
- **Vue 3 Composition API** patterns

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy Options
- **Vercel**: Connect GitHub repo for automatic deployments
- **Netlify**: Drag and drop `dist` folder
- **AWS S3**: Upload build files to S3 bucket
- **Docker**: Use provided Dockerfile for containerization

### Environment Configuration
Update API base URL for production:
```env
VITE_API_BASE_URL=https://your-api-domain.com
```

## 🔍 API Integration

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Users
- `GET /users/profile` - Get user profile
- `GET /users/team` - Get team members (managers)
- `GET /users/managers` - Get all managers

### Feedback
- `GET /feedback/` - Get all feedback
- `POST /feedback/` - Create feedback
- `PUT /feedback/{id}` - Update feedback
- `POST /feedback/{id}/acknowledge` - Acknowledge feedback

### Dashboard
- `GET /dashboard/manager` - Manager dashboard data
- `GET /dashboard/employee` - Employee dashboard data

## 🐛 Troubleshooting

### Common Issues

**API Connection Issues**
- Verify backend is running on port 8000
- Check CORS configuration in backend
- Ensure proxy configuration in vite.config.ts

**Authentication Problems**
- Clear localStorage and try logging in again
- Check JWT token expiration
- Verify user role permissions

**Build Issues**
- Clear node_modules and reinstall dependencies
- Check TypeScript errors with `npm run type-check`
- Verify all imports are correct

## 📄 License

This project is part of the Internal Feedback Tool system. See the main project README for license information.

## 🤝 Contributing

1. Follow the established code style and patterns
2. Add TypeScript types for new features
3. Test on multiple screen sizes
4. Update documentation for new features
5. Ensure accessibility compliance

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the backend API documentation
- Create an issue in the project repository
