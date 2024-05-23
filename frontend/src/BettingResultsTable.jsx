import React, { useEffect, useState } from 'react';
import { Tabs, Table, Progress } from 'antd';
import axios from 'axios';

const { TabPane } = Tabs;

const BettingResultsTabs = () => {
    const [sportData, setSportData] = useState({});
    const [loading, setLoading] = useState(true);
    const [progress, setProgress] = useState(0);

    const fetchData = async () => {
        try {
            setLoading(true);
            const response = await axios.get('http://backend:8000/betting_results');
            setSportData(response.data.reduce((acc, item) => {
                const { sport_name, ...rest } = item;
                if (!acc[sport_name]) {
                    acc[sport_name] = [];
                }
                acc[sport_name].push(rest);
                return acc;
            }, {}));
        } catch (error) {
            console.error("Error fetching data: ", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => {
            setProgress((prevProgress) => {
                if (prevProgress >= 100) {
                    fetchData();
                    return 0;
                }
                return prevProgress + 1;
            });
        }, 300);

        return () => clearInterval(interval); // Очистка интервала при размонтировании компонента
    }, []);

    return (
        <>
            <Progress percent={progress} status="active" />
            <Tabs>
                {Object.entries(sportData).map(([sport, data]) => (
                    <TabPane tab={sport} key={sport}>
                        <Table
                            columns={[
                                { title: 'Команда Дома', dataIndex: 'home', key: 'home' },
                                { title: 'Команда Гости', dataIndex: 'away', key: 'away' },
                                { title: 'Счет', dataIndex: 'score', key: 'score' },
                                { title: 'Счет Дома', dataIndex: 'home_score', key: 'home_score' },
                                { title: 'Счет Гости', dataIndex: 'away_score', key: 'away_score' },
                            ]}
                            dataSource={data}
                            loading={loading}
                            rowKey={(record) => record.url}
                            size='small'
                            pagination={{ pageSize: 20 }} 
                        />
                    </TabPane>
                ))}
            </Tabs>
        </>
    );
};

export default BettingResultsTabs;
