import axios from "axios";

interface Params {
    baseUrl: string;
    method: string;
}

const defaultConfig : Params = {
    baseUrl: "http://localhost",
    method: 'post'
}

export const networkAction = (action:string) => {
    return postAPI(9000, getHandle(action))
}

const getHandle = (action:string) => {
    switch(action) {
        case 'generate_network':
            return 'new-command-node'
        case 'add_mining_node':
            return 'new-mining-node'
        case 'kill_mining_node':
            return 'kill-mining-node'
        case 'kill_network':
            return 'kill-network'
    }
}

export const vote = () => {

}

const postAPI = async (port: number, handle: string): Promise<any> => {
    return await axios({
        ...defaultConfig,
        url: `${defaultConfig.baseUrl}:${port}/${handle}`
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

