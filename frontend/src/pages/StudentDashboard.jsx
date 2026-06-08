import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpen, 
  Award, 
  Bell, 
  FileText, 
  CheckCircle2, 
  Clock, 
  ArrowRight, 
  Search, 
  LogOut, 
  Home, 
  Menu, 
  X, 
  ChevronRight, 
  Sparkles, 
  ThumbsUp, 
  Star,
  BookMarked,
  Activity,
  GraduationCap
} from 'lucide-react';
import api from '../services/api';

export default function StudentDashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/api/student/dashboard');
      if (response.data && response.data.success) {
        setDashboardData(response.data);
      } else {
        throw new Error(response.data.message || 'Failed to load dashboard data.');
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || err.message || 'Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center font-sans text-slate-800 antialiased relative">
        <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
          <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-indigo-100/40 blur-3xl animate-pulse" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] rounded-full bg-violet-100/40 blur-3xl" />
        </div>
        <div className="relative z-10 flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-slate-500 font-medium animate-pulse">Loading workspace...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center font-sans text-slate-800 antialiased relative">
        <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
          <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-indigo-100/40 blur-3xl" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] rounded-full bg-violet-100/40 blur-3xl" />
        </div>
        <div className="relative z-10 bg-white border border-slate-100 rounded-2xl p-8 max-w-md w-full shadow-lg text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto">
            <X size={24} />
          </div>
          <div className="space-y-2">
            <h3 className="font-bold text-slate-900 text-lg">Failed to Load Dashboard</h3>
            <p className="text-sm text-slate-500 leading-relaxed">
              {error}
            </p>
          </div>
          <button onClick={fetchDashboardData} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2.5 rounded-lg text-sm shadow-sm transition-colors">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Parse API Response Data
  const student = dashboardData?.user || {};
  const college = dashboardData?.college;
  const followedSubjects = dashboardData?.followed_subjects || [];
  const recentQuizzes = dashboardData?.recent_quizzes || [];
  const notifications = dashboardData?.notifications_preview || [];
  const communityPicks = dashboardData?.community_preview || [];
  const quickStats = dashboardData?.quick_stats || {};

  const stats = [
    { label: "Followed Subjects", value: quickStats.followed_subjects_count || 0, icon: BookOpen, color: "text-indigo-600 bg-indigo-50 border-indigo-100" },
    { label: "Quizzes Completed", value: quickStats.quizzes_completed_count || 0, icon: Award, color: "text-violet-600 bg-violet-50 border-violet-100" },
    { label: "Unread Alerts", value: quickStats.unread_notifications_count || 0, icon: Bell, color: "text-amber-600 bg-amber-50 border-amber-100" },
    { label: "Resources Shared", value: quickStats.community_uploads_count || 0, icon: FileText, color: "text-emerald-600 bg-emerald-50 border-emerald-100" }
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans text-slate-800 antialiased overflow-hidden w-full relative">
      
      {/* BACKGROUND FLOATING GRADIENT ACCENTS */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-indigo-100/40 blur-3xl animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] rounded-full bg-violet-100/40 blur-3xl" style={{ animationDelay: '2s' }} />
      </div>

      {/* SIDEBAR NAVIGATION (Desktop) */}
      <aside className={`fixed inset-y-0 left-0 w-64 bg-white border-r border-slate-100 z-50 flex flex-col justify-between transform lg:translate-x-0 transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:static shrink-0`}>
        <div>
          {/* Sidebar Header */}
          <div className="h-16 flex items-center justify-between px-6 border-b border-slate-50">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold shadow-md shadow-indigo-100">
                S
              </div>
              <span className="font-semibold text-lg tracking-tight text-slate-900">StudyHub</span>
              <span className="text-xs bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded font-medium">v2.0</span>
            </div>
            <button onClick={() => setSidebarOpen(false)} className="lg:hidden p-1.5 text-slate-500 hover:bg-slate-50 rounded">
              <X size={18} />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1.5">
            <button 
              onClick={() => setActiveTab('dashboard')} 
              className={`w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'dashboard' ? 'bg-indigo-50/70 text-indigo-700' : 'text-slate-600 hover:bg-slate-50'}`}
            >
              <div className="flex items-center gap-3">
                <Home size={18} />
                <span>Dashboard</span>
              </div>
              <ChevronRight size={14} className={activeTab === 'dashboard' ? 'opacity-100' : 'opacity-0'} />
            </button>
            
            <a 
              href="/student/subjects"
              className="w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50 transition-all"
            >
              <div className="flex items-center gap-3">
                <BookOpen size={18} />
                <span>Subjects</span>
              </div>
              <ChevronRight size={14} className="opacity-0 group-hover:opacity-100" />
            </a>

            <a 
              href="/student/community"
              className="w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50 transition-all"
            >
              <div className="flex items-center gap-3">
                <FileText size={18} />
                <span>Community Picks</span>
              </div>
              <ChevronRight size={14} className="opacity-0" />
            </a>

            <a 
              href="/student/notifications"
              className="w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50 transition-all"
            >
              <div className="flex items-center gap-3">
                <Bell size={18} />
                <span>Alerts Center</span>
              </div>
              {quickStats.unread_notifications_count > 0 && (
                <span className="text-xs font-semibold bg-amber-500 text-white rounded-full px-2 py-0.5">
                  {quickStats.unread_notifications_count}
                </span>
              )}
            </a>
          </nav>
        </div>

        {/* Sidebar Footer User Details */}
        <div className="p-4 border-t border-slate-50 bg-slate-50/30">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
              {student.name ? student.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : 'ST'}
            </div>
            <div className="overflow-hidden">
              <h4 className="font-semibold text-sm text-slate-900 truncate">{student.name}</h4>
              <p className="text-xs text-slate-500 truncate">{student.email}</p>
            </div>
          </div>
          <a href="/logout" className="w-full flex items-center gap-2 justify-center px-4 py-2 border border-slate-200 hover:bg-slate-50 rounded-lg text-sm text-slate-600 font-medium transition-colors text-center">
            <LogOut size={16} />
            <span>Logout</span>
          </a>
        </div>
      </aside>

      {/* MAIN CONTAINER WORKSPACE */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden z-10">
        
        {/* HEADER TOOLBAR */}
        <header className="h-16 bg-white border-b border-slate-100 flex items-center justify-between px-6 shrink-0">
          <div className="flex items-center gap-4">
            <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 text-slate-600 hover:bg-slate-50 rounded">
              <Menu size={20} />
            </button>
            
            <div className="relative w-72 hidden md:block">
              <Search className="absolute left-3 top-2.5 text-slate-400" size={16} />
              <input 
                type="text" 
                placeholder="Search tools & courses..."
                disabled
                className="w-full pl-9 pr-4 py-2 bg-slate-50/70 border-0 rounded-lg text-sm transition-all focus:outline-none cursor-not-allowed opacity-60"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* College Badge */}
            {college ? (
              <div className="flex items-center gap-2 border border-slate-100 rounded-full py-1 pl-1 pr-3 bg-slate-50">
                {college.logo_url ? (
                  <img src={college.logo_url} alt="logo" className="w-6 h-6 rounded-full object-cover" />
                ) : (
                  <div className="w-6 h-6 rounded-full bg-indigo-600 text-white text-[10px] font-bold flex items-center justify-center">
                    {college.initials}
                  </div>
                )}
                <span className="text-xs font-semibold text-slate-700 hidden sm:inline truncate max-w-[150px]">
                  {college.name}
                </span>
              </div>
            ) : (
              <a href="/student/onboarding" className="text-xs bg-amber-50 text-amber-700 border border-amber-200 rounded-full px-3 py-1 font-semibold hover:bg-amber-100 transition-colors">
                ⚠️ Select College
              </a>
            )}

            {/* Notification Bell */}
            <a href="/student/notifications" className="p-2 hover:bg-slate-50 rounded-full relative text-slate-600 block">
              <Bell size={20} />
              {quickStats.unread_notifications_count > 0 && (
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-indigo-600 border border-white" />
              )}
            </a>
          </div>
        </header>

        {/* WORKSPACE CONTENT AREA (Scrollable) */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* ONBOARDING PROMPT BANNER (if no college selected) */}
          {!college && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2 text-amber-800 font-semibold">
                  <Sparkles size={18} />
                  <span>Complete Your Profile Setup</span>
                </div>
                <p className="text-amber-700 text-sm">
                  You haven't selected a college yet. Select your college and configure notifications/subjects to start learning.
                </p>
              </div>
              <a href="/student/onboarding" className="bg-amber-600 hover:bg-amber-700 text-white font-semibold text-sm px-5 py-2.5 rounded-lg shadow-sm w-fit transition-colors whitespace-nowrap">
                Setup Profile Now
              </a>
            </motion.div>
          )}

          {/* WELCOME HERO ACCENT CARD */}
          <motion.div 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="relative bg-gradient-to-r from-indigo-900 via-indigo-850 to-violet-900 text-white rounded-2xl p-6 overflow-hidden shadow-lg shadow-indigo-900/10"
          >
            <div className="absolute right-0 top-0 w-64 h-64 bg-gradient-to-bl from-white/10 to-transparent rounded-full blur-2xl pointer-events-none" />
            
            <div className="max-w-2xl relative z-10">
              <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md px-3 py-1 rounded-full text-xs font-medium w-fit mb-4">
                <Sparkles size={12} className="text-indigo-300" />
                <span>Classroom Workspace Active</span>
              </div>
              <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">
                Welcome back, {student.name ? student.name.split(' ')[0] : 'Student'}!
              </h2>
              <p className="text-slate-200 text-sm leading-relaxed mb-5">
                Unlock your course curriculum materials, check off pending chapter quizzes, or explore peer resource uploads.
              </p>
              
              <div className="flex flex-wrap gap-3">
                <a href="/student/quizzes" className="bg-white hover:bg-slate-50 text-indigo-900 font-semibold px-4.5 py-2 rounded-lg text-sm flex items-center gap-2 shadow-sm transition-all hover:translate-x-0.5">
                  <span>Start Quiz Solver</span>
                  <ArrowRight size={16} />
                </a>
                <a href="/student/pyqs" className="bg-white/10 hover:bg-white/20 text-white border border-white/20 font-medium px-4.5 py-2 rounded-lg text-sm transition-colors text-center">
                  Browse PYQ Papers
                </a>
              </div>
            </div>
          </motion.div>

          {/* QUICK STATS ROW */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: idx * 0.05 }}
                className="bg-white border border-slate-100 p-4.5 rounded-xl flex items-center justify-between shadow-sm hover:shadow-md/50 transition-all hover:-translate-y-0.5"
              >
                <div className="space-y-1">
                  <span className="text-xs font-medium text-slate-500">{stat.label}</span>
                  <h3 className="text-2xl font-bold tracking-tight text-slate-900">{stat.value}</h3>
                </div>
                <div className={`w-11 h-11 rounded-lg border flex items-center justify-center ${stat.color}`}>
                  <stat.icon size={20} />
                </div>
              </motion.div>
            ))}
          </div>

          {/* TWO PANEL DASHBOARD GRID */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* LEFT COLUMN (2/3 Width on Desktop) */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* Followed Subjects list */}
              <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <BookMarked size={18} className="text-indigo-600" />
                    <h3 className="font-bold text-slate-900 text-base">Your Followed Subjects</h3>
                  </div>
                  <a href="/student/subjects" className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold flex items-center gap-0.5">
                    <span>Manage</span>
                    <ChevronRight size={14} />
                  </a>
                </div>

                {followedSubjects.length === 0 ? (
                  <div className="border border-dashed border-slate-200 bg-slate-50/50 rounded-xl p-8 text-center space-y-3">
                    <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-500">
                      <BookOpen size={24} />
                    </div>
                    <div className="space-y-1">
                      <h4 className="font-semibold text-slate-900 text-sm">No Followed Subjects</h4>
                      <p className="text-xs text-slate-500 max-w-sm mx-auto">
                        Subscribe to subjects in your college curriculum to access study materials, past year papers, and custom practice quizzes.
                      </p>
                    </div>
                    <a href="/student/subjects" className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xs px-4 py-2 rounded-lg transition-colors">
                      <span>Browse All Subjects</span>
                      <ArrowRight size={14} />
                    </a>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {followedSubjects.map((subject) => (
                      <a 
                        key={subject.id} 
                        href={`/student/subjects/${subject.id}`} 
                        className="border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/5 p-4 rounded-xl space-y-3 shadow-sm/5 hover:shadow-sm transition-all group block"
                      >
                        <div>
                          <span className="text-[10px] font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 rounded px-1.5 py-0.5 uppercase tracking-wider">
                            {subject.code}
                          </span>
                          <h4 className="font-semibold text-sm text-slate-900 mt-2 truncate group-hover:text-indigo-600 transition-colors">
                            {subject.name}
                          </h4>
                        </div>
                        
                        {/* Chapter Progress */}
                        <div className="space-y-1">
                          <div className="flex justify-between text-[11px] text-slate-500 font-medium">
                            <span>Syllabus Progress</span>
                            <span>{subject.progress || 0}%</span>
                          </div>
                          <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                            <div className="bg-indigo-600 h-full rounded-full transition-all duration-500" style={{ width: `${subject.progress || 0}%` }} />
                          </div>
                        </div>

                        <div className="flex items-center justify-between text-xs text-slate-500 font-medium pt-1">
                          <span>{subject.materials_count || 0} Notes</span>
                          <span>{subject.quizzes_count || 0} Quizzes</span>
                        </div>
                      </a>
                    ))}
                  </div>
                )}
              </div>

              {/* Continue Learning Quizzes */}
              <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Activity size={18} className="text-indigo-600" />
                    <h3 className="font-bold text-slate-900 text-base">Continue Learning</h3>
                  </div>
                  {recentQuizzes.length > 0 && (
                    <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-medium">
                      {recentQuizzes.length} Quizzes Available
                    </span>
                  )}
                </div>

                {recentQuizzes.length === 0 ? (
                  <div className="border border-dashed border-slate-200 bg-slate-50/50 rounded-xl p-8 text-center space-y-3">
                    <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-500">
                      <Award size={24} />
                    </div>
                    <div className="space-y-1">
                      <h4 className="font-semibold text-slate-900 text-sm">No Quizzes Available</h4>
                      <p className="text-xs text-slate-500 max-w-sm mx-auto">
                        Your college hasn't published any quizzes yet, or you're not subscribed to subjects with quizzes.
                      </p>
                    </div>
                    <a href="/student/quizzes" className="inline-flex items-center gap-1.5 border border-slate-200 hover:bg-slate-50 text-slate-600 font-medium text-xs px-4 py-2 rounded-lg transition-colors">
                      Explore Quizzes
                    </a>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {recentQuizzes.map((quiz) => (
                      <div key={quiz.id} className="border border-slate-100 hover:border-indigo-100 hover:bg-indigo-50/5 p-4 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="text-[10px] font-bold text-slate-500 bg-slate-100 rounded px-1.5 py-0.5 uppercase">
                              {quiz.subject_code || quiz.subject}
                            </span>
                            <span className={`text-[10px] font-bold rounded px-1.5 py-0.5 uppercase tracking-wider ${quiz.difficulty.toLowerCase() === 'hard' ? 'text-rose-600 bg-rose-50 border border-rose-100' : quiz.difficulty.toLowerCase() === 'medium' ? 'text-amber-600 bg-amber-50 border border-amber-100' : 'text-emerald-600 bg-emerald-50 border border-emerald-100'}`}>
                              {quiz.difficulty} Difficulty
                            </span>
                          </div>
                          <h4 className="font-semibold text-sm text-slate-900 mt-1">
                            {quiz.title}
                          </h4>
                        </div>

                        <div className="flex items-center justify-between md:justify-end gap-6 border-t md:border-0 pt-3 md:pt-0 border-slate-50">
                          <div className="flex items-center gap-4 text-xs text-slate-500 font-medium">
                            <span className="flex items-center gap-1"><Clock size={14} /> {quiz.duration || `${quiz.duration_minutes} mins`}</span>
                            <span className="flex items-center gap-1"><GraduationCap size={14} /> {quiz.question_count || quiz.questions} Questions</span>
                          </div>
                          <a href={`/student/quizzes/${quiz.id}/start`} className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xs px-3.5 py-1.5 rounded-lg shadow-sm transition-colors text-center">
                            Solve Quiz
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

            </div>

            {/* RIGHT COLUMN (1/3 Width on Desktop) */}
            <div className="space-y-6">
              
              {/* Notifications Preview */}
              <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Bell size={18} className="text-indigo-600" />
                    <h3 className="font-bold text-slate-900 text-base">Alerts Center</h3>
                  </div>
                  <a href="/student/notifications" className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold">
                    View All
                  </a>
                </div>

                {notifications.length === 0 ? (
                  <div className="border border-dashed border-slate-200 bg-slate-50/50 rounded-xl p-6 text-center space-y-2">
                    <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
                      <Bell size={20} />
                    </div>
                    <h4 className="font-semibold text-slate-900 text-xs">No New Notifications</h4>
                    <p className="text-[11px] text-slate-500 max-w-xs mx-auto">
                      You're all caught up! New syllabus updates and quiz publications will appear here.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {notifications.map((notif) => (
                      <a 
                        key={notif.id} 
                        href={`/student/notifications/${notif.id}/open`} 
                        className={`block p-3 rounded-lg border text-xs relative overflow-hidden transition-all hover:bg-indigo-50/5 ${notif.isNew ? 'bg-indigo-50/30 border-indigo-100/50' : 'bg-slate-50/30 border-slate-100'}`}
                      >
                        {notif.isNew && (
                          <div className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-600" />
                        )}
                        
                        <div className="flex justify-between items-center gap-2 mb-1.5 pl-1.5">
                          <h4 className="font-bold text-slate-900 truncate">{notif.title}</h4>
                          <span className="text-[10px] text-slate-500 font-medium whitespace-nowrap">
                            {notif.created_at ? new Date(notif.created_at).toLocaleDateString() : ''}
                          </span>
                        </div>
                        
                        <p className="text-slate-600 leading-relaxed pl-1.5 line-clamp-2">
                          {notif.message}
                        </p>
                      </a>
                    ))}
                  </div>
                )}
              </div>

              {/* Community Picks */}
              <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <ThumbsUp size={16} className="text-indigo-600" />
                    <h3 className="font-bold text-slate-900 text-base">Community Picks</h3>
                  </div>
                  <a href="/student/community" className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold">
                    Explore
                  </a>
                </div>

                {communityPicks.length === 0 ? (
                  <div className="border border-dashed border-slate-200 bg-slate-50/50 rounded-xl p-6 text-center space-y-2">
                    <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
                      <ThumbsUp size={18} />
                    </div>
                    <h4 className="font-semibold text-slate-900 text-xs">No Shared Resources</h4>
                    <p className="text-[11px] text-slate-500 max-w-xs mx-auto">
                      Be the first to share notes or guides with your peers in the community library!
                    </p>
                    <a href="/student/community/upload" className="inline-block text-[11px] text-indigo-600 hover:text-indigo-700 font-semibold mt-1">
                      Upload Notes
                    </a>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {communityPicks.map((pick) => (
                      <a 
                        key={pick.id} 
                        href={`/student/community/materials/${pick.id}`} 
                        className="p-3 border border-slate-100 hover:border-slate-200 rounded-lg flex items-center justify-between gap-4 transition-all block"
                      >
                        <div className="overflow-hidden space-y-1">
                          <h4 className="font-semibold text-xs text-slate-900 truncate">
                            {pick.title}
                          </h4>
                          <div className="flex items-center gap-2 flex-wrap text-[10px] text-slate-500 font-medium">
                            <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${pick.type === 'PDF' ? 'text-rose-600 bg-rose-50' : 'text-sky-600 bg-sky-50'}`}>
                              {pick.type}
                            </span>
                            <span className="truncate max-w-[120px]">Uploaded by {pick.uploaded_by || pick.uploader}</span>
                          </div>
                        </div>

                        <div className="flex flex-col items-end shrink-0">
                          <span className="text-[11px] font-bold text-slate-700 flex items-center gap-0.5"><Star size={12} className="text-amber-500 fill-amber-500" /> {pick.rating}</span>
                          <span className="text-[10px] text-slate-500 font-medium">{pick.likes_count || pick.likes} Likes</span>
                        </div>
                      </a>
                    ))}
                  </div>
                )}
              </div>

            </div>

          </div>

        </main>
      </div>

    </div>
  );
}
