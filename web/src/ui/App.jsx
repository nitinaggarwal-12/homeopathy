import React, { useEffect, useState } from 'react'
import './styles.css'
import './i18n'
import { useTranslation } from 'react-i18next'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App(){
  const { t, i18n } = useTranslation()
  const [complaint, setComplaint] = useState('')
  const [search, setSearch] = useState('')
  const [mmResults, setMmResults] = useState([])
  const [repResult, setRepResult] = useState(null)
  const [lang, setLang] = useState('en')

  useEffect(()=>{ i18n.changeLanguage(lang) }, [lang])

  async function doSearch(){
    const res = await fetch(`${API}/mm_search`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ q: search, k: 5 }) })
    const data = await res.json()
    setMmResults(data.results || [])
  }

  async function doRepertorize(){
    const caseObj = {
      presenting_complaint: complaint,
      mental_emotional: [], generals: [], particulars: [], cravings: [], aversions: [], sleep: [], dreams: [], past_history: [], family_history: [], lifestyle: [], red_flags: []
    }
    const res = await fetch(`${API}/repertorize`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ case: caseObj }) })
    const data = await res.json()
    setRepResult(data)
  }

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto">
      <header className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{t('title')}</h1>
          <p className="text-gray-600">{t('subtitle')}</p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm">{t('language')}</label>
          <select className="border rounded px-2 py-1" value={lang} onChange={e=>setLang(e.target.value)}>
            <option value="en">{t('english')}</option>
            <option value="hi">{t('hindi')}</option>
          </select>
        </div>
      </header>

      <section className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl shadow p-4">
          <h2 className="font-semibold mb-2">{t('presentingComplaint')}</h2>
          <textarea className="w-full border rounded p-2 h-28" placeholder={t('presentingComplaint')} value={complaint} onChange={e=>setComplaint(e.target.value)} />
          <button className="mt-3 bg-black text-white rounded-xl px-4 py-2" onClick={doRepertorize}>{t('repertorize')}</button>

          <div className="mt-4">
            {repResult && (
              <pre className="text-xs bg-gray-50 border rounded p-3 overflow-auto max-h-80">{JSON.stringify(repResult, null, 2)}</pre>
            )}
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow p-4">
          <h2 className="font-semibold mb-2">{t('materiaSearch')}</h2>
          <input className="w-full border rounded p-2" placeholder={t('searchPlaceholder')} value={search} onChange={e=>setSearch(e.target.value)} />
          <button className="mt-3 bg-black text-white rounded-xl px-4 py-2" onClick={doSearch}>{t('materiaSearch')}</button>
          <div className="mt-4 space-y-3">
            {mmResults.length === 0 ? (
              <p className="text-gray-500">{t('noResults')}</p>
            ) : mmResults.map((r, idx)=>(
              <div key={idx} className="border rounded-xl p-3">
                <div className="font-semibold">{r.title} <span className="text-xs text-gray-500">({r.similarity.toFixed(3)})</span></div>
                <pre className="text-xs whitespace-pre-wrap">{r.excerpt}</pre>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="mt-10 text-xs text-gray-500">
        <p><strong>Disclaimer:</strong> Educational guidance only; not a substitute for professional medical care. In emergencies, seek immediate help.</p>
      </footer>
    </div>
  )
}
