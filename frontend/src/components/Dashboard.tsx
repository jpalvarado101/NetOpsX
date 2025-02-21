import React from 'react';

interface Transaction {
  id: number;
  status: string;
  route: string;
  created_at?: string;
}

interface DashboardProps {
  transactions: Transaction[];
}

const Dashboard: React.FC<DashboardProps> = ({ transactions }) => {
  return (
    <div>
      <h2>Transaction Feed</h2>
      <table border={1} cellPadding={5} cellSpacing={0}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Route</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(tx => (
            <tr key={tx.id}>
              <td>{tx.id}</td>
              <td>{tx.status}</td>
              <td>{tx.route}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
