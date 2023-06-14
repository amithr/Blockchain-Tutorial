import React, {FC, useContext, useState, useEffect, useLayoutEffect} from 'react'




interface Block {
    chainIndex:number;
    powNum:number;
    prevHash:string;
    voterPubKey:number;
    voterHash:string;
    vote:string;
    timeStamp:number;
}

interface BlockProps {
    block:Block;
}

const Block: FC<BlockProps> = (block) => {
    return(
        <>
        
        </>
    );
};

export default Block;