import { memo, useMemo } from 'react';
import { type EdgeProps, BaseEdge, getBezierPath } from 'reactflow';
import styles from './QuantumEdge.module.css';

const QuantumEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
}: EdgeProps) => {
  // 1. Get the standard Bezier path for the interaction/hit area (invisible but clickable)
  const [bezierPath] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetPosition,
    targetX,
    targetY,
  });

  // 2. Generate the "Wavy" path for the visual representation
  // We'll generate a sine wave along the straight line between source and target for V1.
  // (Doing a sine wave along a Bezier curve is complex math for a V1)
  const wavyPath = useMemo(() => {
    const dx = targetX - sourceX;
    const dy = targetY - sourceY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    // Config
    const amplitude = 5; // Height of the wave
    const frequency = 0.1; // How tight the waves are
    const segments = Math.max(10, Math.floor(distance / 5)); // Resolution

    let path = `M ${sourceX} ${sourceY}`;

    // Calculate normal vector for the wave offset
    // Normal to (dx, dy) is (-dy, dx)
    const nx = -dy / distance;
    const ny = dx / distance;

    for (let i = 1; i <= segments; i++) {
      const t = i / segments;

      // Point on the straight line
      const lx = sourceX + dx * t;
      const ly = sourceY + dy * t;

      // Sine wave offset
      // We use Math.sin(t * distance * frequency)
      const waveOffset = Math.sin(t * distance * frequency) * amplitude;

      // Final point
      const px = lx + nx * waveOffset;
      const py = ly + ny * waveOffset;

      // Use quadratic bezier for smoother curves between points? 
      // Or just LineTo (L) if resolution is high enough. L is safer for SVG size.
      path += ` L ${px} ${py}`;
    }

    return path;
  }, [sourceX, sourceY, targetX, targetY]);

  return (
    <>
      {/* Invisible thick path for easier clicking/hovering */}
      <BaseEdge
        path={bezierPath}
        style={{ strokeWidth: 20, stroke: 'transparent', fill: 'none' }}
        interactionWidth={20}
      />

      {/* The Visual Quantum Wavy Path */}
      <path
        id={id}
        style={style}
        className={styles.quantumEdgePath}
        d={wavyPath}
        markerEnd={markerEnd}
      />
    </>
  );
};

export default memo(QuantumEdge);
