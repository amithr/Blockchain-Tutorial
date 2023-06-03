import { useContext} from 'react'
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from "react-router-dom";
import jwt_decode from "jwt-decode";
import { UserContext, UserDataType } from './contexts/UserContext'
import './App.css'

function App() {
  const {userData, setUserData} = useContext(UserContext);
  const navigate = useNavigate();
  return (
    <>
      <h1>Welcome to the Blockchain Playground</h1>
        <GoogleLogin
          onSuccess={(credentialResponse:any) => {
              let googleUserData:UserDataType = jwt_decode(credentialResponse.credential);
              setUserData(googleUserData);
              navigate("/dashboard")
          }}
          onError={() => {
              console.log('Login Failed');
          }}
          useOneTap
          auto_select
        />
    </>
  )
}

export default App
