import React, { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("https://mental-health-checkin-production.up.railway.app/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Une erreur est survenue." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-pink-50 p-6 text-gray-800">
      <h1 className="text-3xl font-bold text-center mb-8">Mental Health Check-in 💖</h1>

      <Tabs defaultValue="prediction" className="max-w-2xl mx-auto">
        <TabsList className="grid grid-cols-2 bg-pink-200">
          <TabsTrigger value="prediction">💬 Prédiction</TabsTrigger>
          <TabsTrigger value="about">📖 À propos</TabsTrigger>
        </TabsList>

        <TabsContent value="prediction">
          <Card className="bg-white rounded-2xl shadow-lg p-4 mt-4">
            <CardContent>
              <label className="block mb-2 font-semibold">Comment vous sentez-vous aujourd'hui ?</label>
              <Input
                placeholder="Exprimez votre humeur..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="mb-4 border-pink-300"
              />
              <Button onClick={handleSubmit} disabled={loading} className="bg-pink-400 hover:bg-pink-500 text-white">
                {loading ? "Analyse en cours..." : "Analyser"}
              </Button>
              {result && (
                <div className="mt-4 p-4 rounded-xl bg-pink-100 border border-pink-300">
                  {result.error ? (
                    <p className="text-red-500">{result.error}</p>
                  ) : (
                    <>
                      <p className="font-medium">Texte : {result.message}</p>
                      <p className="font-bold text-pink-700">
                        😊 Émotion détectée : {result.predicted_emotion}
                      </p>
                    </>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="about">
          <Card className="bg-white rounded-2xl shadow-lg p-4 mt-4">
            <CardContent>
              <p className="text-md">
                Cette application vous permet de faire un check-in quotidien de votre état émotionnel.
                Elle analyse votre texte et prédit une émotion à partir de notre modèle NLP. Prenez soin de vous ✨
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  );
}
