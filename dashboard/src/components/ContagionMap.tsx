import { useRef, useEffect } from 'react';
import { ForceGraph3D } from 'react-force-graph';
import * as THREE from 'three';

interface Node {
    id: string;
    tier: number;
    isCritical: boolean;
}

interface Link {
    source: string;
    target: string;
    value: number;
}

interface ContagionData {
    nodes: Node[];
    links: Link[];
}

interface ContagionMapProps {
    data: ContagionData;
    onNodeClick: (node: Node) => void;
}

const ContagionMap = ({ data, onNodeClick }: ContagionMapProps) => {
    const fgRef = useRef<any>(null);

    useEffect(() => {
        if (fgRef.current) {
            fgRef.current.d3Force('link').distance((l: any) => (l.value || 1) * 50);
        }
    }, [data]);

    return (
        <ForceGraph3D
            ref={fgRef}
            graphData={data}
            nodeLabel="id"
            nodeAutoColorBy="tier"
            linkColor={() => '#444'}
            linkDirectionalParticles={2}
            linkDirectionalParticleSpeed={(d: any) => (d.value || 1) * 0.01}
            nodeThreeObject={(node: any) => {
                const color = node.isCritical ? '#ff4d4d' :
                    node.tier === 1 ? '#00d4ff' :
                        node.tier === 2 ? '#00ffcc' : '#ffcc00';

                const obj = new THREE.Mesh(
                    new THREE.SphereGeometry(node.isCritical ? 7 : 5),
                    new THREE.MeshLambertMaterial({
                        color: color,
                        emissive: color,
                        emissiveIntensity: node.isCritical ? 0.8 : 0.2
                    })
                );
                return obj;
            }}
            backgroundColor="#050505"
            onNodeClick={(node: any) => onNodeClick(node as Node)}
        />
    );
};

export default ContagionMap;
