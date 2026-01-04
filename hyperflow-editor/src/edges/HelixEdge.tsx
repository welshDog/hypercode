import React, { useMemo } from 'react';
import { type EdgeProps, getBezierPath } from 'reactflow';
import styles from './HelixEdge.module.css';

const HelixEdge: React.FC<EdgeProps> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
}) => {
  // Calculate the base path (straight or bezier) to guide the helix
  // We use a simple straight line math for the helix logic, but we could curve it.
  // For simplicity and robustness, let's calculate the sine waves along the vector.

  const [edgePath] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const paths = useMemo(() => {
    const dx = targetX - sourceX;
    const dy = targetY - sourceY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    // Helix configuration
    const amplitude = 8; // Width of the helix
    const frequency = 0.2; // How tight the twist is
    const segments = Math.max(20, Math.floor(distance / 4)); // Resolution

    let pathA = `M ${sourceX} ${sourceY}`;
    let pathB = `M ${sourceX} ${sourceY}`;
    let rungs = '';

    // Normal vector for amplitude direction (perpendicular to the line)
    // For a straight line approach:
    const nx = -dy / distance;
    const ny = dx / distance;

    for (let i = 1; i <= segments; i++) {
      const t = i / segments;

      // Linear interpolation point
      const lx = sourceX + dx * t;
      const ly = sourceY + dy * t;

      // Sine wave calculation
      // Phase shift of PI for the second strand
      const phaseA = t * distance * frequency;
      const phaseB = t * distance * frequency + Math.PI;

      const offsetA = Math.sin(phaseA) * amplitude;
      const offsetB = Math.sin(phaseB) * amplitude;

      const pxA = lx + nx * offsetA;
      const pyA = ly + ny * offsetA;

      const pxB = lx + nx * offsetB;
      const pyB = ly + ny * offsetB;

      pathA += ` L ${pxA} ${pyA}`;
      pathB += ` L ${pxB} ${pyB}`;

      // Add rungs every few segments
      if (i % 2 === 0) {
        rungs += ` M ${pxA} ${pyA} L ${pxB} ${pyB}`;
      }
    }

    return { pathA, pathB, rungs };
  }, [sourceX, sourceY, targetX, targetY]);

  return (
    <>
      {/* Invisible hover path for easier selection */}
      <path
        d={edgePath}
        strokeWidth={20}
        stroke="transparent"
        fill="none"
        style={{ cursor: 'pointer' }}
      />

      {/* Rungs (Hydrogen Bonds) */}
      <path
        d={paths.rungs}
        className={styles.rungs}
        fill="none"
      />

      {/* Strand A (5' to 3') */}
      <path
        id={`${id}-strandA`}
        d={paths.pathA}
        className={`${styles.helixPath} ${styles.strandA}`}
        markerEnd={markerEnd}
        style={style}
      />

      {/* Strand B (3' to 5') */}
      <path
        id={`${id}-strandB`}
        d={paths.pathB}
        className={`${styles.helixPath} ${styles.strandB}`}
        style={style}
      />
    </>
  );
};

export default HelixEdge;
