console.log("Sanity Check");

// Get Stripe publishable key

fetch("/payments/config/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        //Initializing Stripe
        const stripe = Stripe(data.publicKey);

        document.querySelector("#submitBtn").addEventListener("click", () => {
            fetch("/payments/create-checkout-session")
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    console.log(data);
                    return stripe.redirectToCheckout({ sessionId: data.sessionId });
                })
                .then((res) => {
                    console.log(res);
                });
        });
    });