import { memo } from 'react';
import { Handle, Position, type NodeProps } from 'reactflow';
import styles from './HexNode.module.css';

const HexNode = ({ data, selected }: NodeProps) => {
  return (
    <div
      className={`${styles.hexContainer} ${selected ? styles.selected : ''}`}
      tabIndex={0} // Accessibility: Focusable
      aria-label={data.label}
    >
      <div className={styles.hexContent}>
        {/* Top Handle (Input) */}
        <Handle
          type="target"
          position={Position.Top}
          className={styles.handleTop}
        />

        <div className={styles.label}>
          {data.label}
        </div>

        {/* Bottom Handle (Output) */}
        <Handle
          type="source"
          position={Position.Bottom}
          className={styles.handleBottom}
        />
      </div>

      {/* SVG Hexagon Background */}
      <svg className={styles.hexBg} viewBox="0 0 100 100" preserveAspectRatio="none">
        <polygon points="50 0, 100 25, 100 75, 50 100, 0 75, 0 25" />
      </svg>
    </div>
  );
};

export default memo(HexNode);
