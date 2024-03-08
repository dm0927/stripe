// Create a Stripe client.

const submitPayment = document.getElementById('submit-payment');
const paymentDataCollection = document.getElementById('payment-data-collection');
const paymentProcessing = document.getElementById('payment-processing');
const amountToBeCollected = document.getElementById('amount-to-be-collected');
const amountToBeShown = document.getElementById('amount-to-be-shown');
const cancelPayment = document.getElementById('cancel-payment');

var amount = 0;

submitPayment.addEventListener('click', function() {
    paymentDataCollection.classList.add('d-none');
    paymentProcessing.classList.remove('d-none');
    amount = amountToBeCollected.value;
    amountToBeShown.innerHTML = `$${amount}`;
});

cancelPayment.addEventListener('click', function() {
    paymentProcessing.classList.add('d-none');
    paymentDataCollection.classList.remove('d-none');
    amountToBeCollected.value = ''
})

document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe('pk_test_51OdtYMDAoP6ChPNAwR1VUFxVMg6EEneUtJ5E1a3o8l24kgKIkeWKfOGOkwGOKFOZnd23Vn76OOUbLue4CT0nWQPd00ZyzkWSUS');
    var elements = stripe.elements();

    console.log("stripe: ", stripe)

    // var cardNumber = elements.create('cardNumber', { style: style });
    let cardNumber = elements.create("cardNumber", {
                        showIcon: true,
                        placeholder: "Card Number",
                        iconStyle: "solid",
                        classes: {
                            base: "form-control",
                        },
                        style: {
                        base: {
                                iconColor: "blue",
                                fontSize: "16px",
                            },
                        },
                    });
    cardNumber.mount('#card-number');

    let cardExpiryElement = elements.create("cardExpiry", {
                                classes: {
                                    base: "form-control",
                                },
                                style: {
                                base: {
                                        fontSize: "16px",
                                    },
                                },
                            });
    cardExpiryElement.mount('#card-expiry');

    var cardCvcElement = elements.create("cardCvc", {
                            classes: {
                            base: "form-control",
                            },
                            style: {
                            base: {
                                fontSize: "16px",
                            },
                            },
                        });
    cardCvcElement.mount('#card-cvc');
});