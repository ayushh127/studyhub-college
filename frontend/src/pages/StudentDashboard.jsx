import React, { useState } from 'react';
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

export default function StudentDashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');

  // Mock Data
  const student = {
    name: "Ayush Sharma",
    email: "student@timing.com",
    college: "Institute of Technology & Science",
    code: "ITS_DELHI",
    logoInitials: "ITS"
  };

  const stats = [
    { label: "Followed Subjects", value: 5, icon: BookOpen, color: "text-indigo-600 bg-indigo-50 border-indigo-100" },
    { label: "Quizzes Completed", value: 14, icon: Award, color: "text-violet-600 bg-violet-50 border-violet-100" },
    { label: "Unread Alerts", value: 3, icon: Bell, color: "text-amber-600 bg-amber-50 border-amber-100" },
    { label: "Resources Shared", value: 4, icon: FileText, color: "text-emerald-600 bg-emerald-50 border-emerald-100" }
  ];

  const followedSubjects = [
    { id: 1, name: "Database Management Systems", code: "DBMS-401", progress: 75, materials: 14, quizzes: 4 },
    { id: 2, name: "Operating Systems", code: "OS-402", progress: 40, materials: 9, quizzes: 3 },
    { id: 3, name: "Computer Networks", code: "CN-403", progress: 60, materials: 11, quizzes: 5 }
  ];

  const recentQuizzes = [
    { id: 101, title: "SQL Normalization Practice", subject: "DBMS-401", difficulty: "Medium", duration: "15 mins", questions: 10 },
    { id: 102, title: "CPU Scheduling Algorithms", subject: "OS-402", difficulty: "Hard", duration: "20 mins", questions: 12 }
  ];

  const communityPicks = [
    { id: 201, title: "SQL Joins Visual Cheatsheet.pdf", type: "PDF", subject: "DBMS", uploader: "Priya V.", likes: 24, rating: 4.9 },
    { id: 202, title: "TCP/IP 3-Way Handshake Guide", type: "Link", subject: "CN", uploader: "Rohan S.", likes: 18, rating: 4.7 }
  ];

  const notifications = [
    { id: 301, title: "New Quiz Available", message: "Operating Systems Unit 3: Deadlocks quiz has been published.", time: "10 mins ago", isNew: true, subjectCode: "OS-402" },
    { id: 302, title: "Study Material Uploaded", message: "DBMS Unit 5: Transaction Management notes are now online.", time: "1 hour ago", isNew: true, subjectCode: "DBMS-401" },
    { id: 303, title: "PYQ Paper Added", message: "2024 End-Semester Computer Networks PYQ is now available.", time: "2 hours ago", isNew: false, subjectCode: "CN-403" }
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans text-slate-800 antialiased overflow-hidden">
      
      {/* BACKGROUND FLOATING GRADIENT ACCENTS */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-indigo-100/40 blur-3xl animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] rounded-full bg-violet-100/40 blur-3xl" style={{ animationDelay: '2s' }} />
      </div>

      {/* SIDEBAR NAVIGATION (Desktop) */}
      <aside className={`fixed inset-y-0 left-0 w-64 bg-white border-r border-slate-100 z-50 flex flex-col justify-between transform lg:translate-x-0 transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:static`}>
        <div>
          {/* Sidebar Header */}
          <div className="h-16 flex items-center justify-between px-6 border-b border-slate-50">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold shadow-md shadow-indigo-100">
                S
              </div>
              <span className="font-semibold text-lg tracking-tight text-slate-900">StudyHub</span>
              <span className="text-xs bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded font-medium">v1.0</span>
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
            
            <button 
              onClick={() => setActiveTab('subjects')} 
              className={`w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'subjects' ? 'bg-indigo-50/70 text-indigo-700' : 'text-slate-600 hover:bg-slate-50'}`}
            >
              <div className="flex items-center gap-3">
                <BookOpen size={18} />
                <span>Subjects</span>
              </div>
              <ChevronRight size={14} className={activeTab === 'subjects' ? 'opacity-100' : 'opacity-0'} />
            </button>

            <button 
              onClick={() => setActiveTab('community')} 
              className={`w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'community' ? 'bg-indigo-50/70 text-indigo-700' : 'text-slate-600 hover:bg-slate-50'}`}
            >
              <div className="flex items-center gap-3">
                <FileText size={18} />
                <span>Community Picks</span>
              </div>
              <ChevronRight size={14} className={activeTab === 'community' ? 'opacity-100' : 'opacity-0'} />
            </button>

            <button 
              onClick={() => setActiveTab('alerts')} 
              className={`w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'alerts' ? 'bg-indigo-50/70 text-indigo-700' : 'text-slate-600 hover:bg-slate-50'}`}
            >
              <div className="flex items-center gap-3">
                <Bell size={18} />
                <span>Alerts Center</span>
              </div>
              {stats[2].value > 0 && (
                <span className="text-xs font-semibold bg-amber-500 text-white rounded-full px-2 py-0.5">
                  {stats[2].value}
                </span>
              )}
            </button>
          </nav>
        </div>

        {/* Sidebar Footer User Details */}
        <div className="p-4 border-t border-slate-50 bg-slate-50/30">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
              AS
            </div>
            <div className="overflow-hidden">
              <h4 className="font-semibold text-sm text-slate-900 truncate">{student.name}</h4>
              <p className="text-xs text-slate-500 truncate">{student.email}</p>
            </div>
          </div>
          <button className="w-full flex items-center gap-2 justify-center px-4 py-2 border border-slate-200 hover:bg-slate-50 rounded-lg text-sm text-slate-600 font-medium transition-colors">
            <LogOut size={16} />
            <span>Logout</span>
          </button>
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
                placeholder="Search subjects, units, notes..."
                className="w-full pl-9 pr-4 py-2 bg-slate-50 hover:bg-slate-100/70 focus:bg-white border-0 focus:ring-1.5 focus:ring-indigo-500 rounded-lg text-sm transition-all focus:outline-none"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* College Badge */}
            <div className="flex items-center gap-2 border border-slate-100 rounded-full py-1 pl-1 pr-3 bg-slate-50">
              <div className="w-6 h-6 rounded-full bg-indigo-600 text-white text-[10px] font-bold flex items-center justify-center">
                {student.logoInitials}
              </div>
              <span className="text-xs font-semibold text-slate-700 hidden sm:inline truncate max-w-[150px]">
                {student.college}
              </span>
            </div>

            {/* Notification Bell */}
            <button className="p-2 hover:bg-slate-50 rounded-full relative text-slate-600">
              <Bell size={20} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-indigo-600 border border-white" />
            </button>
          </div>
        </header>

        {/* WORKSPACE CONTENT AREA (Scrollable) */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* WELCOME HERO ACCENT CARD */}
          <motion.div 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="relative bg-gradient-to-r from-indigo-900 via-indigo-850 to-violet-900 text-white rounded-2xl p-6 overflow-hidden shadow-lg shadow-indigo-900/10"
          >
            {/* Ambient inner gradients */}
            <div className="absolute right-0 top-0 w-64 h-64 bg-gradient-to-bl from-white/10 to-transparent rounded-full blur-2xl pointer-events-none" />
            
            <div className="max-w-2xl relative z-10">
              <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md px-3 py-1 rounded-full text-xs font-medium w-fit mb-4">
                <Sparkles size={12} className="text-indigo-300" />
                <span>Classroom Workspace Active</span>
              </div>
              <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">
                Welcome back, {student.name.split(' ')[0]}!
              </h2>
              <p className="text-slate-200 text-sm leading-relaxed mb-5">
                Unlock your course curriculum materials, check off pending chapter quizzes, or explore peer resource uploads.
              </p>
              
              <div className="flex flex-wrap gap-3">
                <button className="bg-white hover:bg-slate-50 text-indigo-900 font-semibold px-4.5 py-2 rounded-lg text-sm flex items-center gap-2 shadow-sm transition-all hover:translate-x-0.5">
                  <span>Start Quiz Solver</span>
                  <ArrowRight size={16} />
                </button>
                <button className="bg-white/10 hover:bg-white/20 text-white border border-white/20 font-medium px-4.5 py-2 rounded-lg text-sm transition-colors">
                  Browse PYQ Papers
                </button>
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
                  <button className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold flex items-center gap-0.5">
                    <span>Manage</span>
                    <ChevronRight size={14} />
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {followedSubjects.map((subject) => (
                    <div key={subject.id} className="border border-slate-100 hover:border-slate-200 p-4 rounded-xl space-y-3 shadow-sm/5 hover:shadow-sm transition-all group">
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
                          <span>{subject.progress}%</span>
                        </div>
                        <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                          <div className="bg-indigo-600 h-full rounded-full" style={{ width: `${subject.progress}%` }} />
                        </div>
                      </div>

                      <div className="flex items-center justify-between text-xs text-slate-500 font-medium pt-1">
                        <span>{subject.materials} Notes</span>
                        <span>{subject.quizzes} Quizzes</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Continue Learning Quizzes */}
              <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Activity size={18} className="text-indigo-600" />
                    <h3 className="font-bold text-slate-900 text-base">Continue Learning</h3>
                  </div>
                  <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-medium">
                    2 Pending Quizzes
                  </span>
                </div>

                <div className="space-y-3">
                  {recentQuizzes.map((quiz) => (
                    <div key={quiz.id} className="border border-slate-100 hover:border-indigo-100 hover:bg-indigo-50/5 p-4 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-[10px] font-bold text-slate-500 bg-slate-100 rounded px-1.5 py-0.5 uppercase">
                            {quiz.subject}
                          </span>
                          <span className={`text-[10px] font-bold rounded px-1.5 py-0.5 uppercase tracking-wider ${quiz.difficulty === 'Hard' ? 'text-rose-600 bg-rose-50 border border-rose-100' : 'text-amber-600 bg-amber-50 border border-amber-100'}`}>
                            {quiz.difficulty} Difficulty
                          </span>
                        </div>
                        <h4 className="font-semibold text-sm text-slate-900 mt-1">
                          {quiz.title}
                        </h4>
                      </div>

                      <div className="flex items-center justify-between md:justify-end gap-6 border-t md:border-0 pt-3 md:pt-0 border-slate-50">
                        <div className="flex items-center gap-4 text-xs text-slate-500 font-medium">
                          <span className="flex items-center gap-1"><Clock size={14} /> {quiz.duration}</span>
                          <span className="flex items-center gap-1"><GraduationCap size={14} /> {quiz.questions} Questions</span>
                        </div>
                        <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xs px-3.5 py-1.5 rounded-lg shadow-sm transition-colors">
                          Solve Quiz
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
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
                  <button className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold">
                    View All
                  </button>
                </div>

                <div className="space-y-3">
                  {notifications.map((notif) => (
                    <div key={notif.id} className={`p-3 rounded-lg border text-xs relative overflow-hidden transition-all ${notif.isNew ? 'bg-indigo-50/30 border-indigo-100/50' : 'bg-slate-50/30 border-slate-100'}`}>
                      {/* Left border indicator for new notifications */}
                      {notif.isNew && (
                        <div className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-600" />
                      )}
                      
                      <div className="flex justify-between items-center gap-2 mb-1.5 pl-1.5">
                        <h4 className="font-bold text-slate-900 truncate">{notif.title}</h4>
                        <span className="text-[10px] text-slate-500 font-medium whitespace-nowrap">{notif.time}</span>
                      </div>
                      
                      <p className="text-slate-600 leading-relaxed pl-1.5 line-clamp-2">
                        {notif.message}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Community Picks */}
              <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <ThumbsUp size={16} className="text-indigo-600" />
                    <h3 className="font-bold text-slate-900 text-base">Community Picks</h3>
                  </div>
                  <button className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold">
                    Explore
                  </button>
                </div>

                <div className="space-y-3">
                  {communityPicks.map((pick) => (
                    <div key={pick.id} className="p-3 border border-slate-100 hover:border-slate-200 rounded-lg flex items-center justify-between gap-4 transition-all">
                      <div className="overflow-hidden space-y-1">
                        <h4 className="font-semibold text-xs text-slate-900 truncate">
                          {pick.title}
                        </h4>
                        <div className="flex items-center gap-2 flex-wrap text-[10px] text-slate-500 font-medium">
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${pick.type === 'PDF' ? 'text-rose-600 bg-rose-50' : 'text-sky-600 bg-sky-50'}`}>
                            {pick.type}
                          </span>
                          <span>Uploaded by {pick.uploader}</span>
                        </div>
                      </div>

                      <div className="flex flex-col items-end shrink-0">
                        <span className="text-[11px] font-bold text-slate-700 flex items-center gap-0.5"><Star size={12} className="text-amber-500 fill-amber-500" /> {pick.rating}</span>
                        <span className="text-[10px] text-slate-500 font-medium">{pick.likes} Likes</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>

        </main>
      </div>

    </div>
  );
}
