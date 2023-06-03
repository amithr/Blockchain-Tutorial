import React, {FC, useContext} from 'react'
import ReactDOM from 'react-dom/client';
import { UserContext } from '../contexts/UserContext';

interface DashboardProps {
    userId?:string;
}

const Dashboard: FC<DashboardProps> = () => {
    const {userData, setUserData} = useContext(UserContext);

    return(
        <>
            <h1>This is a dashboard.</h1>
            <h2>{userData.email}</h2>
        </>
    );
};
export default Dashboard;