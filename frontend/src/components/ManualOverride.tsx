import React, { useState } from 'react';
import { manualOverride } from '../services/api';

const ManualOverride: React.FC = () => {
  const [transactionId, setTransactionId] = useState<number | "">("");
  const [newRoute, setNewRoute] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (transactionId && newRoute) {
      await manualOverride(Number(transactionId), newRoute);
      setTransactionId("");
      setNewRoute("");
      alert("Override submitted");
    }
  };

  return (
    <div>
      <h2>Manual Override</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Transaction ID:
          <input 
            type="number" 
            value={transactionId}
            onChange={e => setTransactionId(e.target.value === "" ? "" : Number(e.target.value))}
            required
          />
        </label>
        <br />
        <label>
          New Route:
          <input 
            type="text" 
            value={newRoute}
            onChange={e => setNewRoute(e.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Submit Override</button>
      </form>
    </div>
  );
};

export default ManualOverride;
