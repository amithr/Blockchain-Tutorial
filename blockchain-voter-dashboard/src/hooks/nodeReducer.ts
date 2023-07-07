export const nodeReducer = (state, action) => {
    switch (action.type) {
        case 'SET_COMMAND_NODE':
        return { ...state, commandNode: action.payload };
        case 'ADD_MESSAGE':
        return { ...state, messages: [...state.messages, action.payload] };
        case 'SET_BLOCKCHAIN':
        return { ...state, blockchain: action.payload };
        case 'SET_PREV_MESSAGE':
        return { ...state, prevMessage: action.payload };
        case 'ADD_NODE':
        return { ...state, nodes: [...state.nodes, action.payload] };
        case 'REMOVE_NODE':
        return { ...state, nodes: state.nodes.filter((node) => node !== action.payload) };
        default:
        return state;
    }
};