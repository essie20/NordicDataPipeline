import type { LucideIcon } from "lucide-react";
import { cn } from "../lib/utils";
import { motion } from "framer-motion";

interface StatCardProps {
    title: string;
    value: string;
    change?: string;
    icon: LucideIcon;
    trend?: "up" | "down" | "neutral";
    className?: string;
    color?: string; // e.g. "text-blue-500"
}

export function StatCard({ title, value, change, icon: Icon, trend, className, color = "text-blue-400" }: StatCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={cn(
                "bg-zinc-900/50 backdrop-blur-md border border-zinc-800 p-6 rounded-xl hover:border-zinc-700 transition-colors shadow-lg",
                className
            )}
        >
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium text-zinc-400">{title}</p>
                    <h3 className="text-3xl font-bold text-white mt-1 tracking-tight">{value}</h3>
                </div>
                <div className={cn("p-3 rounded-lg bg-zinc-800/50", color)}>
                    <Icon size={24} />
                </div>
            </div>
            {change && (
                <div className="mt-4 flex items-center text-sm">
                    <span
                        className={cn(
                            "font-medium px-2 py-0.5 rounded-full text-xs",
                            trend === "up" ? "bg-green-500/10 text-green-400" :
                                trend === "down" ? "bg-red-500/10 text-red-400" : "bg-zinc-500/10 text-zinc-400"
                        )}
                    >
                        {change}
                    </span>
                    <span className="text-zinc-500 ml-2">vs last 24h</span>
                </div>
            )}
        </motion.div>
    );
}
