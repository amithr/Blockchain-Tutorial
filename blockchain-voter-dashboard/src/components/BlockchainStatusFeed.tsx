import React, {FC, useContext, useState, useEffect, useLayoutEffect} from 'react';
import Block from './Block';

type BlockchainStatusFeedProps = {
    blockchain:[];
}

const BlockchainStatusFeed: FC<BlockchainStatusFeedProps> = ({blockchain}) => {
    return(
        <>
            {blockchain.map((block, index) => (
                <Block key={index} block={block} transaction={block.transaction} />
            ))}
        </>
    );
};

export default BlockchainStatusFeed;