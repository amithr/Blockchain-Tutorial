import React, {FC, useContext, useState, useEffect, useLayoutEffect} from 'react'




interface Block {
    chain_index:number;
    proof_of_work_number:number;
    previous_hash:string;
    timestamp:number;
}

interface Transaction {
    voter_public_key_x:string;
    voter_public_key_y:number;
    voter_hash:string;
    vote:string;
}

type BlockProps = {
    block:Block;
    transaction:Transaction

}

const Block: FC<BlockProps> = ({block, transaction}) => {
    return(
        <>
            <p>Chain Index: {block.chain_index}</p>
            <p>Previous Hash: {block.previous_hash}</p>
            <p>Vote: {transaction.vote}</p>
            <p>Timestamp: {block.timestamp}</p>
        </>
    );
};

export default Block;