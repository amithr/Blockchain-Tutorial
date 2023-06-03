import { createContext, useState, FC, PropsWithChildren} from 'react';

export interface UserDataType {
    email: string;
    family_name: string;
    given_name: string;
    picture_url: string;
    email_verified: boolean;
};

type UserContextType = {
    userData: UserDataType;
    setUserData: (userData: UserDataType) => void;
}

export const UserContext = createContext<UserContextType>(null);

const UserProvider: FC<PropsWithChildren> = ({children}) => {
    const [userData, setUserData] = useState<UserDataType>({
        email: "",
        family_name: "",
        given_name: "",
        picture_url: "",
        email_verified: false 
    });

    const userContextValue : UserContextType = {
        userData,
        setUserData
    };

    return(
        <UserContext.Provider value={userContextValue}>
            {children}
        </UserContext.Provider>
    ); 
}

export default UserProvider;