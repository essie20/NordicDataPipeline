import {
    Activity,
    ArrowUpRight,
    BarChart3,
    Battery,
    Zap,
    Database,
    Server,
    RefreshCw
} from "lucide-react";
import { StatCard } from "./StatCard";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { motion } from "framer-motion";

// Mock data
const chartData = [
    { time: "00:00", price: 12.5, consumption: 8500 },
    { time: "04:00", price: 10.2, consumption: 7800 },
    { time: "08:00", price: 45.8, consumption: 10500 },
    { time: "12:00", price: 38.4, consumption: 11200 },
    { time: "16:00", price: 42.1, consumption: 10800 },
    { time: "20:00", price: 25.6, consumption: 9500 },
    { time: "23:59", price: 15.3, consumption: 8900 },
];

export function Dashboard() {
    return (
        <div className="min-h-screen bg-[#09090b] text-white p-8 font-sans selection:bg-cyan-500/30">
            <div className="max-w-7xl mx-auto space-y-8">
                {/* Header */}
                <header className="flex items-center justify-between mb-12">
                    <div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                            NordicDataFlow
                        </h1>
                        <p className="text-zinc-400 mt-2 text-lg">Real-time Energy Market Analytics</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2 px-4 py-2 bg-zinc-900 rounded-full border border-zinc-800">
                            <span className="relative flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                            </span>
                            <span className="text-sm font-medium text-zinc-300">Live Pipeline</span>
                        </div>
                        <button className="p-2 hover:bg-zinc-800 rounded-lg transition-colors border border-transparent hover:border-zinc-700">
                            <RefreshCw className="w-5 h-5 text-zinc-400" />
                        </button>
                    </div>
                </header>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <StatCard
                        title="Avg Spot Price"
                        value="32.4 €/MWh"
                        change="+12.5%"
                        trend="up"
                        icon={Zap}
                        color="text-yellow-400"
                    />
                    <StatCard
                        title="Total Consumption"
                        value="10.8 GWh"
                        change="-2.1%"
                        trend="down"
                        icon={Activity}
                        color="text-cyan-400"
                    />
                    <StatCard
                        title="Grid Frequency"
                        value="50.02 Hz"
                        change="0.0%"
                        trend="neutral"
                        icon={Battery}
                        color="text-green-400"
                    />
                    <StatCard
                        title="Data Points"
                        value="1.2M"
                        change="+8.4%"
                        trend="up"
                        icon={Database}
                        color="text-purple-400"
                    />
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">

                    {/* Main Chart */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.1 }}
                        className="lg:col-span-2 bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-6 shadow-xl"
                    >
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold flex items-center gap-2">
                                <BarChart3 className="w-5 h-5 text-blue-400" />
                                Price vs Consumption
                            </h2>
                            <div className="flex gap-2">
                                {['24h', '7d', '30d'].map((period) => (
                                    <button
                                        key={period}
                                        className="px-3 py-1 text-xs font-medium bg-zinc-800 hover:bg-zinc-700 rounded-md text-zinc-400 hover:text-white transition-all"
                                    >
                                        {period}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="h-[400px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={chartData}>
                                    <defs>
                                        <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                        </linearGradient>
                                        <linearGradient id="colorCons" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                                    <XAxis
                                        dataKey="time"
                                        stroke="#71717a"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                    />
                                    <YAxis
                                        stroke="#71717a"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                        tickFormatter={(value) => `${value}`}
                                    />
                                    <Tooltip
                                        contentStyle={{
                                            backgroundColor: '#18181b',
                                            borderColor: '#27272a',
                                            borderRadius: '8px',
                                            color: '#fff'
                                        }}
                                        itemStyle={{ color: '#fff' }}
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="price"
                                        stroke="#3b82f6"
                                        strokeWidth={3}
                                        fillOpacity={1}
                                        fill="url(#colorPrice)"
                                        name="Price (€/MWh)"
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="consumption"
                                        stroke="#06b6d4"
                                        strokeWidth={3}
                                        fillOpacity={1}
                                        fill="url(#colorCons)"
                                        name="Consumption (MW)"
                                        yAxisId={1}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </motion.div>

                    {/* Side Panel: Pipeline Status */}
                    <div className="space-y-6">
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.2 }}
                            className="bg-zinc-900/50 backdrop-blur-sm border border-zinc-800 rounded-2xl p-6"
                        >
                            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                <Server className="w-5 h-5 text-purple-400" />
                                System Health
                            </h2>

                            <div className="space-y-6">
                                <StatusItem label="API Ingestion (Fingrid)" status="operational" latency="45ms" />
                                <StatusItem label="API Ingestion (Eurostat)" status="operational" latency="120ms" />
                                <StatusItem label="Data Lake (Silver)" status="operational" latency="12ms" />
                                <StatusItem label="SQL Warehouse (Gold)" status="processing" latency="85ms" />
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.3 }}
                            className="bg-gradient-to-br from-blue-900/20 to-zinc-900 border border-blue-900/30 rounded-2xl p-6"
                        >
                            <h3 className="text-lg font-medium text-blue-200 mb-2">Did you know?</h3>
                            <p className="text-sm text-blue-300/80 leading-relaxed">
                                NordicDataFlow processes over 1.2 million data points daily, correlating energy prices with weather patterns across 4 countries.
                            </p>
                            <button className="mt-4 text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1 font-medium transition-colors">
                                View Documentation <ArrowUpRight className="w-4 h-4" />
                            </button>
                        </motion.div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatusItem({ label, status, latency }: { label: string, status: "operational" | "degraded" | "down" | "processing", latency: string }) {
    const color =
        status === "operational" ? "bg-green-500" :
            status === "processing" ? "bg-blue-500" :
                status === "degraded" ? "bg-yellow-500" : "bg-red-500";

    return (
        <div className="flex items-center justify-between group">
            <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${color} shadow-[0_0_8px_rgba(0,0,0,0.5)] shadow-${color}/50`} />
                <span className="text-zinc-300 text-sm font-medium group-hover:text-white transition-colors">{label}</span>
            </div>
            <span className="text-xs text-zinc-500 font-mono">{latency}</span>
        </div>
    )
}
