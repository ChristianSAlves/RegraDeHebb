"use client";

import { useState } from 'react';
import axios from 'axios';
import { AxiosError } from 'axios';

type Matrix = number[][];

export default function Home() {
    const [matrix, setMatrix] = useState<Matrix>(Array(10).fill(0).map(() => Array(10).fill(0)));
    const [result, setResult] = useState<string>('');

    const handleClick = (rowIdx: number, colIdx: number) => {
        const newMatrix = matrix.map((row, rIdx) => 
            row.map((cell, cIdx) => (rIdx === rowIdx && cIdx === colIdx ? 1 : cell))
        );
        setMatrix(newMatrix);
    };

    const handleTrain = async () => {
        try {
            const response = await axios.post('http://localhost:8000/hebb/api/train/');
            console.log(response.data);
        } catch (error) {
            console.error('Erro no treinamento:', error);
        }
    };

    const handleRecognize = async () => {
        try {
            const response = await axios.post('http://localhost:8000/hebb/api/recognize/', { matrix: matrix.flat() });
            // Exibir o resultado retornado pela API
            setResult(response.data.result);
            console.log('Letra reconhecida:', response.data.result);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error('Erro no reconhecimento:', error.response?.data || error.message);
            } else {
                console.error('Erro inesperado:', error);
            }
        }
    };

    return (
        <div>
            <h1>Reconhecimento de Letras</h1>
            <div>
                {matrix.map((row, rowIdx) => (
                    <div key={rowIdx} style={{ display: 'flex' }}>
                        {row.map((cell, colIdx) => (
                            <div
                                key={colIdx}
                                onClick={() => handleClick(rowIdx, colIdx)}
                                style={{
                                    width: 20,
                                    height: 20,
                                    backgroundColor: cell ? 'black' : 'white',
                                    border: '1px solid gray',
                                    cursor: 'pointer',
                                }}
                            />
                        ))}
                    </div>
                ))}
            </div>
            <button onClick={handleTrain}> Treinar o modelo</button>
            <button onClick={handleRecognize}>Reconhecer Letra</button>
            {result && <p>Letra Reconhecida: {result}</p>}
        </div>
    );
}

