import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Research from './pages/Research'
import Results from './pages/Results'
import Team from './pages/Team'

function App() {
  return (
    <div className="min-h-screen bg-page text-text-primary">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/research" element={<Research />} />
        <Route path="/results" element={<Results />} />
        <Route path="/team" element={<Team />} />
      </Routes>
      <Footer />
    </div>
  )
}

export default App
