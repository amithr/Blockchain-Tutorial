import axios from "axios";

interface Params {
    baseUrl: string;
    method: string;
}

const defaultConfig : Params = {
    baseUrl: "http://localhost",
    method: 'post'
}

export const networkAction = (action:string, data:any) => {
    const response = postAPI(9000, getHandle(action), data)
    console.log(data)
    return response
}

const getHandle = (action:string) => {
    switch(action) {
        case 'generate_network':
            return 'new-network'
        case 'add_mining_node':
            return 'new-mining-node'
        case 'kill_mining_node':
            return 'kill-node'
        case 'kill_network':
            return 'kill-network'
    }
}

export const vote = () => {

}

const postAPI = async (port: number, handle: string, data:any): Promise<any> => {
    return await axios({
        ...defaultConfig,
        url: `${defaultConfig.baseUrl}:${port}/${handle}`,
        data
    }).then ( (response) => {
        console.log(response)
        return {
            status: response.status,
            data: response.data
        }
    }).catch((error) =>{
        console.log(error)
        return {
            status: error.status,
            data: error.response
        }
    })
}

