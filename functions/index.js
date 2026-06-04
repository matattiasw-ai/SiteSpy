const { onCall, onRequest, HttpsError } = require("firebase-functions/v2/https");

exports.health = onRequest((request, response) => {
  response.json({
    ok: true,
    app: "SiteSpy",
    service: "firebase-functions"
  });
});

exports.prepareEstimateReport = onCall((request) => {
  if (!request.auth) {
    throw new HttpsError("unauthenticated", "Sign in before preparing reports.");
  }

  const estimate = request.data?.estimate || {};
  return {
    userId: request.auth.uid,
    totalCost: Number(estimate.totalCost || 0),
    estimatedUnits: Number(estimate.estimatedUnits || 0),
    note: "Report formatting helper only. The mobile app calculates and saves estimates client-side."
  };
});
