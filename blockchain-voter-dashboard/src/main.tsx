import React from 'react'
import ReactDOM from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import App from './App.tsx'
import Dashboard from './pages/Dashboard.tsx'
import { GoogleOAuthProvider } from '@react-oauth/google';
import UserProvider from './contexts/UserContext.tsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path:"/dashboard/",
    element: <Dashboard />,
  }
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
      <GoogleOAuthProvider clientId="623093186468-a24aaumofhj3d51ntkqn9dv37sg6q3q8.apps.googleusercontent.com">
        <UserProvider >
          <RouterProvider router={router} />
        </UserProvider>
      </GoogleOAuthProvider>
  </React.StrictMode>,
)
